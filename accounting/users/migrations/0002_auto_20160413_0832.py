# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.DecimalField(default=0.0, verbose_name='\u0421\u0447\u0435\u0442 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f \u0432 \u0440\u0443\u0431\u043b\u044f\u0445', max_digits=14, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='individual_tax_number',
            field=models.CharField(max_length=20, verbose_name='\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u043d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0439 \u043d\u043e\u043c\u0435\u0440', blank=True),
        ),
    ]
