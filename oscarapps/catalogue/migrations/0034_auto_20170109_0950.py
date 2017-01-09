# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-09 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0033_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, null=True, to='catalogue.Colors', verbose_name='Color(s)'),
        ),
    ]