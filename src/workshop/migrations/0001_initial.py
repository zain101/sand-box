# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2016-12-23 07:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profileapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activityName', models.CharField(max_length=200)),
                ('activityType', models.CharField(max_length=200)),
                ('schedule', models.DateTimeField()),
                ('information', models.CharField(blank=True, max_length=500)),
                ('content', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, upload_to=b'')),
                ('terms', models.TextField(blank=True)),
                ('confirmation', models.BooleanField(default=False)),
                ('cost', models.FloatField(default=0.0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileapp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venueName', models.CharField(max_length=500)),
                ('summary', models.CharField(max_length=1000)),
                ('website', models.URLField(blank=True)),
                ('socialLink', models.URLField(blank=True)),
                ('coverPhoto', models.ImageField(blank=True, upload_to=b'')),
                ('logo', models.ImageField(blank=True, upload_to=b'')),
                ('contactInfo', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=15)),
                ('gmailCalender', models.CharField(blank=True, max_length=500)),
                ('confirmation', models.BooleanField(default=False)),
                ('wifiAvailability', models.BooleanField(default=False)),
                ('capacity', models.IntegerField(default=0)),
                ('cateringAvailability', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Venue'),
        ),
    ]
