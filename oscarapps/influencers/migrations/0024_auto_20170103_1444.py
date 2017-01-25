# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-03 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0023_auto_20170103_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='influencers',
            name='state_or_country',
            field=models.CharField(default='state or country', help_text='Enter your State (USA only) or Country (International only)', max_length=200, verbose_name='Location'),
        ),
    ]
