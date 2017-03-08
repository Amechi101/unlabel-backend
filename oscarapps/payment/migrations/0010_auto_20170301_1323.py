# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-01 13:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20170301_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripecredential',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Stripe Id'),
        ),
        migrations.AlterField(
            model_name='stripecredential',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stripe_credential', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]