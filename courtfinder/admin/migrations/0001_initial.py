# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-08 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=4096, null=True)),
                ('image', models.CharField(max_length=255)),
                ('image_description', models.CharField(max_length=255)),
                ('image_file_path', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]