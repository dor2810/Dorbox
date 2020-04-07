# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-02 15:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('folders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolderMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(default='reader', max_length=126)),
            ],
        ),
        migrations.RemoveField(
            model_name='editor',
            name='editor',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='folder',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='folder',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='reader',
        ),
        migrations.AlterField(
            model_name='folder',
            name='folders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder_folders', to='folders.Folder'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_folders', to='groups.Group'),
        ),
        migrations.DeleteModel(
            name='Editor',
        ),
        migrations.DeleteModel(
            name='Reader',
        ),
        migrations.AddField(
            model_name='foldermember',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_folders', to='folders.Folder'),
        ),
        migrations.AddField(
            model_name='foldermember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
