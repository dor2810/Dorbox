# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()

from folders.models import Folder
from files.models import File

class Group(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User, through='GroupMember')
    pending_members = models.ManyToManyField(User, through='AskedMember', related_name="pendings")
    admin = models.ForeignKey(User, related_name="group_admin", null=True)
    type = models.CharField(max_length=32, default="group")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('groups:all')



    class Meta:
        ordering = ['name']


class AskedMember(models.Model):
    username = models.CharField(max_length = 256, default = '')
    group = models.ForeignKey(Group, related_name = 'pending_list')
    user = models.ForeignKey(User, related_name ='group_pending')

    def get_absolute_url(self, *args, **kwargs):
        return reverse('groups:all')

class GroupMember(models.Model):
    permission = models.CharField(max_length=126,default='reader')
    group = models.ForeignKey(Group, related_name = 'memberships')
    user = models.ForeignKey(User, related_name ='group_users')

    def __str__(self):
        return self.user.username
