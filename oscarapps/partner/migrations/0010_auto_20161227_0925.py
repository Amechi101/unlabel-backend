# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0009_auto_20161227_0640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Style')),
                ('description', models.TextField(blank=True, default=b'', verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Style',
                'verbose_name_plural': 'Styles',
            },
        ),
        migrations.AddField(
            model_name='partner',
            name='style_Preference',
            field=models.ManyToManyField(blank=True, to='partner.Style', verbose_name='Style'),
        ),
    ]
