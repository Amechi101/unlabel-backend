# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 05:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_auto_20160107_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='partneraddress',
            name='description',
            field=models.TextField(blank=True, default=b'', verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='partneraddress',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='partneraddress',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Check to activate brand', verbose_name='Brand Active'),
        ),
        migrations.AddField(
            model_name='partneraddress',
            name='sex_type',
            field=models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female'), (b'B', b'Both')], default=b'B', max_length=1),
        ),
        migrations.AddField(
            model_name='partneraddress',
            name='slug',
            field=models.SlugField(blank=True, default=b'', max_length=255, verbose_name='Brand Slug'),
        ),
        migrations.AddField(
            model_name='partneraddress',
            name='website_url',
            field=models.URLField(blank=True, default=b'', max_length=100, verbose_name='Website'),
        ),
    ]