# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-20 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filing',
            name='accepted',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]