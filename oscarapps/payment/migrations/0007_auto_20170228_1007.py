# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-28 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_auto_20170228_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandcommission',
            name='amount',
            field=models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Commission received'),
        ),
        migrations.AlterField(
            model_name='influencercommission',
            name='amount',
            field=models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Commission received'),
        ),
        migrations.AlterField(
            model_name='payout',
            name='total_amount',
            field=models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Total Amount Transferred'),
        ),
        migrations.AlterField(
            model_name='unlabelcommission',
            name='amount',
            field=models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Commission received'),
        ),
    ]
