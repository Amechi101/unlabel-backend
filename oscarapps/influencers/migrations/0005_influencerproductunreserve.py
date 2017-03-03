# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-03 06:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0013_auto_20170221_0921'),
        ('influencers', '0004_auto_20170227_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfluencerProductUnreserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_unreserved', models.DateTimeField(auto_now_add=True, verbose_name='Product Reserved Date')),
                ('type', models.TextField(choices=[('SELF', 'SELF'), ('SYS', 'SYS')])),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='influencers.Influencers', verbose_name='Influencer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name_plural': 'Influencer Product-Unreserve',
            },
        ),
    ]