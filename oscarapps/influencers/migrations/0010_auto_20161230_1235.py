# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-30 12:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0009_auto_20161230_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='industry',
            options={},
        ),
        migrations.RemoveField(
            model_name='industry',
            name='description',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='name',
        ),
    ]
