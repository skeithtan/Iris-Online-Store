# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-25 06:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity_management', '0004_merge_20170724_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricehistory',
            name='effective_to',
        ),
    ]
