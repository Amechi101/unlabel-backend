# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-02 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0035_auto_20170102_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='brand_feature_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=b'media/uploads', verbose_name='Image'),
        ),
    ]
