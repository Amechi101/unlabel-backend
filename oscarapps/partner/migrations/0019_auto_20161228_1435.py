# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-28 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0018_auto_20161228_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='style_Preference',
            field=models.ManyToManyField(blank=True, to='partner.Style', verbose_name='Style'),
        ),
        migrations.AlterField(
            model_name='style',
            name='name',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='Name'),
        ),
    ]
