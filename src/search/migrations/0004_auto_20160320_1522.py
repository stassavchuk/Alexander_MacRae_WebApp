# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-20 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20160320_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filing',
            name='accepted',
            field=models.DateTimeField(null=True),
        ),
    ]