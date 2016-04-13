# -*- coding: utf-8 -*-

from django import forms

from .models import User


class MoneyTransferForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
    )
    individual_tax_number = forms.CharField(
        required=True,
    )
    amount = forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        required=True,
        min_value=0,
    )

    def clean(self):
        if not self._errors:
            cleaned_data = super(MoneyTransferForm, self).clean()
            sender = cleaned_data.get('user')
            individual_tax_number = cleaned_data.get('individual_tax_number')
            amount = cleaned_data.get('amount')

            recipients = User.objects.filter(individual_tax_number=individual_tax_number)
            if not recipients:
                raise forms.ValidationError(
                    {'individual_tax_number': u'Пользователей с таким ИНН не существует'}
                )
            else:
                cleaned_data.update({'recipients': recipients})

            if sender.balance < amount:
                raise forms.ValidationError(
                    {'amount': u'У пользователя недостаточно средств'}
                )

            if sender.individual_tax_number == individual_tax_number:
                raise forms.ValidationError(
                    {'user': u'Нельзя осуществить перевод самому себе'}
                )

            return cleaned_data

    def transfer_process(self):
        sender = self.cleaned_data.get('user')
        recipients = self.cleaned_data.get('recipients')
        amount = self.cleaned_data.get('amount')

        sender.money_transfer(recipients, amount)
