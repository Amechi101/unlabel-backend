# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-06 08:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0007_auto_20170328_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='influencers',
            name='location',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='influencer_location', to='address.Locations', verbose_name='Location'),
        ),
    ]