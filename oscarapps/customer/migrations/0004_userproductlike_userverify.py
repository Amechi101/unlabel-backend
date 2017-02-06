# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-06 04:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0010_auto_20170206_0453'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0003_update_email_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProductLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product_Like',
                'verbose_name_plural': 'Product_Likes',
            },
        ),
        migrations.CreateModel(
            name='UserVerify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_code', models.TextField(max_length=11)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Verification',
            },
        ),
    ]
