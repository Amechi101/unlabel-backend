# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0012_auto_20161227_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='category',
            field=models.ManyToManyField(blank=True, to='catalogue.Category', verbose_name='Category'),
        ),
    ]