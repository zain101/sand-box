# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2016-12-21 10:03
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0007_auto_20161221_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='topic',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None),
        ),
    ]
