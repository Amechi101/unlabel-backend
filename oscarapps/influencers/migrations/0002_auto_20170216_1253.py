# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-16 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='influencerproductrenteddetails',
            name='influencer',
        ),
        migrations.RemoveField(
            model_name='influencerproductrenteddetails',
            name='product',
        ),
        migrations.AddField(
            model_name='influencerproductreserve',
            name='date_rented',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Product Reserved Date'),
        ),
        migrations.DeleteModel(
            name='InfluencerProductRentedDetails',
        ),
    ]
