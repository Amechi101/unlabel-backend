# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0026_auto_20161227_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]