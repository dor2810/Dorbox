# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-03 10:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0007_auto_20200403_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='last_changer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
