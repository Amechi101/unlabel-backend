# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-14 05:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_userbrandlike_userinfluencerlike'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfluencerlike',
            old_name='Influencer',
            new_name='influencer',
        ),
    ]
