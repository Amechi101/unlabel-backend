# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-28 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0021_style_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='name',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='Style   lksdlkdjf'),
        ),
    ]