# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-09 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0010_auto_20170206_0453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='created',
        ),
        migrations.RemoveField(
            model_name='category',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='product',
            name='asin_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='gcid_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='gtnn_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='information',
        ),
        migrations.RemoveField(
            model_name='product',
            name='ups_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='wieght',
        ),
        migrations.AlterField(
            model_name='product',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='material_info',
            field=models.TextField(blank=True, default='', verbose_name='Material & Care Information'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.PositiveIntegerField(blank=True, max_length=10, null=True, verbose_name='Product weight information'),
        ),
    ]
