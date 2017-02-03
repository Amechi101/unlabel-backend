# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-01 15:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0002_auto_20170125_0546'),
        ('catalogue', '0011_auto_20170201_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfluencerInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('code', models.CharField(max_length=20)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('is_used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='InfluencerProductReserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reserved', models.DateTimeField(auto_now_add=True, verbose_name='Product Reserved Date')),
            ],
            options={
                'verbose_name_plural': 'Influencer Product Reservations',
            },
        ),
        migrations.CreateModel(
            name='Influencers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('auto_id', models.CharField(blank=True, default='', max_length=16, null=True, unique=True, verbose_name='Influencer ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Influencers')),
                ('bio', models.TextField(blank=True, default='', verbose_name='Bio')),
                ('height', models.DecimalField(blank=True, decimal_places=3, default='', help_text='US Measurements', max_digits=10, null=True, verbose_name='Height')),
                ('chest_or_bust', models.DecimalField(blank=True, decimal_places=3, default='', help_text='US Measurements', max_digits=10, null=True, verbose_name='Chest or Bust')),
                ('hips', models.DecimalField(blank=True, decimal_places=3, default='', help_text='US Measurements', max_digits=10, null=True, verbose_name='hips')),
                ('waist', models.DecimalField(blank=True, decimal_places=3, default='', help_text='US Measurements', max_digits=10, null=True, verbose_name='waist')),
                ('location', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='address.Locations', verbose_name='Location')),
                ('users', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='influencers', to=settings.AUTH_USER_MODEL, verbose_name='Users')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='influencerproductreserve',
            name='influencer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='influencers.Influencers', verbose_name='Influencer'),
        ),
        migrations.AddField(
            model_name='influencerproductreserve',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product', verbose_name='Product'),
        ),
    ]
