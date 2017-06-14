# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-07 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_auto_20170404_0747'),
        ('users', '0005_user_influencer_industry'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.Country'),
        ),
        migrations.AddField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]