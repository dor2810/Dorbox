# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-03 09:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_groupmember_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='type',
            field=models.CharField(default='group', max_length=32),
        ),
    ]
