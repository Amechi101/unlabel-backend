# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 09:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0012_auto_20161227_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='created_date',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='modified_date',
            new_name='modified',
        ),
    ]