# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-12 06:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0008_auto_20170111_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locations',
            options={'verbose_name': 'Location', 'verbose_name_plural': 'Locations'},
        ),
    ]
