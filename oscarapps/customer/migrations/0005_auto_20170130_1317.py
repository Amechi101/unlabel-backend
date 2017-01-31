# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-30 13:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0004_userproductlike_userverify'),
        ('catalogue', '0010_auto_20170130_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='userverify',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userproductlike',
            name='product_like',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product'),
        ),
        migrations.AddField(
            model_name='userproductlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]