# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-11 14:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20180811_1514'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FbEvent',
        ),
    ]
