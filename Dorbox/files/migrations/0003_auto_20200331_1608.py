# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-31 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20200331_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='storage/'),
        ),
    ]