# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-28 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0020_auto_20161228_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
