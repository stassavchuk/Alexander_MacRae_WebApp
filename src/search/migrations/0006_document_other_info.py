# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-30 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20160330_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='other_info',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
