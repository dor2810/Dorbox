# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-31 12:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_editors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('folders', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder_folders', to='folders.Folder')),
                ('group', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_folders', to='groups.Group')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reader_folders', to='folders.Folder')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_readers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='editor',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editor_folders', to='folders.Folder'),
        ),
    ]
