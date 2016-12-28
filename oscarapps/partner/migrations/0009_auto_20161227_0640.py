# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0008_auto_20161227_0624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partneraddress',
            name='description',
        ),
        migrations.RemoveField(
            model_name='partneraddress',
            name='image',
        ),
        migrations.RemoveField(
            model_name='partneraddress',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='partneraddress',
            name='sex_type',
        ),
        migrations.RemoveField(
            model_name='partneraddress',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='partneraddress',
            name='website_url',
        ),
        migrations.AddField(
            model_name='partner',
            name='description',
            field=models.TextField(blank=True, default=b'', verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='partner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='partner',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Check to activate brand', verbose_name='Brand Active'),
        ),
        migrations.AddField(
            model_name='partner',
            name='sex_type',
            field=models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female'), (b'B', b'Both')], default=b'B', max_length=1, verbose_name='Sex Type'),
        ),
        migrations.AddField(
            model_name='partner',
            name='slug',
            field=models.SlugField(blank=True, default=b'', max_length=255, verbose_name='Brand Slug'),
        ),
        migrations.AddField(
            model_name='partner',
            name='website_url',
            field=models.URLField(blank=True, default=b'', max_length=100, verbose_name='Website'),
        ),
    ]
