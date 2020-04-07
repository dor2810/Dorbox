# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-01 13:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0004_askedmember_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_editors', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editor_groups', to='groups.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reader_groups', to='groups.Group')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_readers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]