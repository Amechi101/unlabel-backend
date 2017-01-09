# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-06 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_emailconfirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='email',
            field=models.EmailField(max_length=250, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='key',
            field=models.CharField(max_length=255, verbose_name='Hash Key'),
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='link_expired',
            field=models.BooleanField(default=False, verbose_name='Link Expired'),
        ),
    ]