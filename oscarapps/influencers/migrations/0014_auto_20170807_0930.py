# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-07 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0013_auto_20170807_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='name',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
