# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not username:
            msg = _("Это обязательное поле")
            raise ValueError(msg)
        if not email:
            msg = _("Это обязательное поле")
            raise ValueError(msg)
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username, email=email,
            is_staff=False, is_active=True, is_admin=False,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name=_("Имя пользователя"),
        max_length=255,
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=255,
        unique=True,
        db_index=True,
    )
    firstname = models.CharField(
        verbose_name=_("Имя"), max_length=50, blank=True
    )
    lastname = models.CharField(
        verbose_name=_("Фамилия"), max_length=50, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    individual_tax_number = models.CharField(
        verbose_name=_("Индивидуальный налоговый номер"),
        max_length=20,
        blank=True
    )
    balance = models.DecimalField(
        verbose_name=_("Счет пользователя в рублях"),
        decimal_places=2,
        max_digits=14,
        default=0.00
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def money_transfer(self, recipients, amount):
        self.balance -= amount
        self.save()
        share = amount / len(recipients)
        for recipient in recipients:
            recipient.balance += share
            recipient.save()

    def get_short_name(self):
        return self.username
