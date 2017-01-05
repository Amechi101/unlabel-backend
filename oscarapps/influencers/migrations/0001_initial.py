# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-26 12:50
from __future__ import unicode_literals

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import oscarapps.influencers.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=200, unique=True, verbose_name='City')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
            bases=(oscarapps.influencers.mixins.ValidateModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Influencers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, default='', max_length=100, verbose_name='Influencer name')),
                ('instagram_handle', models.CharField(blank=True, default='', max_length=100, verbose_name='Instagram handle')),
                ('instagram_url', models.URLField(blank=True, default='', max_length=255, verbose_name='Instagram url')),
                ('website_url', models.URLField(blank=True, default='', max_length=255, verbose_name='Website url')),
                ('website_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Website name')),
                ('website_isActive', models.BooleanField(default=False, help_text='Check to activate website', verbose_name='Website active')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=100, null=True, verbose_name='Influencer Image')),
                ('photographer_credit', models.CharField(blank=True, default='', help_text='To give credit for photographer for image', max_length=255, verbose_name='Photographer credit')),
                ('photographer_credit_isActive', models.BooleanField(default=False, help_text='Check to activate photographer credit', verbose_name='Photographer credit active')),
                ('question_brand_attraction', models.TextField(blank=True, default='', verbose_name='Brand attraction')),
                ('question_product_favorite_name', models.CharField(blank=True, default='', max_length=255, verbose_name='Favorite product name')),
                ('question_product_favorite_explanation', models.TextField(blank=True, default='', verbose_name='Favorite product explanation')),
                ('question_product_favorite_url', models.URLField(blank=True, default='', max_length=255, verbose_name='Favorite product url')),
                ('question_product_favorite_product_pairing', models.TextField(blank=True, default='', verbose_name='Product pairing explanation')),
                ('question_personal_style_one', models.CharField(blank=True, default='', max_length=255, verbose_name='Personal style 1')),
                ('question_fashion_advice', models.TextField(blank=True, default='', verbose_name='Fashion advice')),
                ('question_favorite_season', models.TextField(blank=True, default='', verbose_name='Favorite season')),
                ('slug', models.SlugField(blank=True, default='', max_length=255, verbose_name='Influencer Slug')),
                ('influencer_isActive', models.BooleanField(default=False, help_text='Check to activate influencer', verbose_name='Influencer active')),
                ('brands', models.ForeignKey(blank=True, default='', help_text='Please select your brand', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='applications.Brand', verbose_name='Brand name')),
                ('hometown', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='influencers.City', verbose_name='Hometown')),
            ],
            options={
                'verbose_name': 'Influencer',
                'verbose_name_plural': 'Influencers',
            },
        ),
        migrations.CreateModel(
            name='StateCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, default='', help_text='Enter your State (USA only) or Country (International only)', max_length=200, unique=True, verbose_name='Location')),
                ('location_choice', models.CharField(blank=True, choices=[('State', 'U.S.A'), ('Country', 'International')], max_length=100, verbose_name='U.S.A or International')),
            ],
            options={
                'verbose_name': 'State or Country',
                'verbose_name_plural': 'State or Country',
            },
            bases=(oscarapps.influencers.mixins.ValidateModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='city',
            name='state_or_country',
            field=models.ForeignKey(blank=True, help_text='Select your state or country', null=True, on_delete=django.db.models.deletion.CASCADE, to='influencers.StateCountry', verbose_name='State or Country'),
        ),
    ]
