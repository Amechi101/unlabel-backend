# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-02 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0014_auto_20170102_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='name',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='Industry Preference'),
        ),
    ]