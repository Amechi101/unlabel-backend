# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-06 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0037_auto_20170102_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='brand_description',
            field=models.TextField(blank=True, default='', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='brand_feature_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='uploads', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='brand_website_url',
            field=models.URLField(blank=True, default='', max_length=100, verbose_name='Website'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='sex_type',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')], default='B', max_length=1, verbose_name='Sex Type'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, verbose_name='Brand Slug'),
        ),
        migrations.AlterField(
            model_name='style',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Description'),
        ),
    ]
