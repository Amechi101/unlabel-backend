# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-24 09:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0006_auto_20170216_1330'),
        ('order', '0005_update_email_length'),
        ('influencers', '0003_auto_20170216_1255'),
        ('payment', '0004_commissionconfiguration'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandCommission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Commission received')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partner.Partner', verbose_name='Brand')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InfluencerCommission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Commission received')),
                ('influencer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='influencers.Influencers', verbose_name='Influencer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UnlabelCommission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Commission received')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='Order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]