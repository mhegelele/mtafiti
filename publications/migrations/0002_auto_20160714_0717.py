# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='keywords',
            field=models.CharField(max_length=512, verbose_name='Research Area'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(max_length=512, unique=True, verbose_name='Title'),
        ),
    ]
