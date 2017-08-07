# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-07 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0005_telephonecode'),
        ('users', '0010_remove_user_influencer_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='telephone_code',
        ),
        migrations.AddField(
            model_name='user',
            name='telephone_code',
            field=models.ManyToManyField(blank=True, null=True, to='address.TelephoneCode'),
        ),
    ]