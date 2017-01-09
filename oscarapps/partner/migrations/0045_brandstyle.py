# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-09 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0044_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Style')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('type', models.ManyToManyField(blank=True, to='partner.BrandStoreType', verbose_name='Brand Store Type')),
            ],
            options={
                'verbose_name': 'Brand Style',
                'verbose_name_plural': 'Brand Styles',
            },
        ),
    ]