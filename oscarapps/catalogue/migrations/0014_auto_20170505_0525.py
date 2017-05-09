# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-05 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0013_auto_20170221_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rental_status',
            field=models.CharField(choices=[('REN', 'Rented'), ('RET', 'Returned'), ('R', 'Reserved'), ('U', 'Unreserved')], default='U', max_length=3, verbose_name='Rental status'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('L', 'Live')], default='D', max_length=1, verbose_name='Status'),
        ),
    ]