# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-01 21:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0005_auto_20200401_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(default='reader', max_length=126)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_files', to='files.File')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='editor',
            name='editor',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='file',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='file',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='reader',
        ),
        migrations.DeleteModel(
            name='Editor',
        ),
        migrations.DeleteModel(
            name='Reader',
        ),
    ]