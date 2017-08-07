# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-02 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0012_influencers_follows'),
        ('catalogue', '0014_auto_20170505_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='influencer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='influencers.Influencers', verbose_name='Influencer Reserved'),
        ),
    ]