# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-28 14:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0024_auto_20161228_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='style',
            name='name',
        ),
    ]
