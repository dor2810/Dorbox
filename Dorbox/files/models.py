# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify

#from groups.models import Group


from django.contrib.auth import get_user_model
User = get_user_model()

class File(models.Model):
    name = models.CharField(max_length=128,unique=True)
    file = models.FileField(upload_to="")
    slug = models.SlugField(allow_unicode=True, unique=True)
    admin = models.ForeignKey(User, related_name ='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True,null=True)
    description = models.TextField(blank = True)
    group = models.ForeignKey('groups.Group', related_name='group_files' ,blank=True, null=True)
    folder = models.ForeignKey('folders.Folder',related_name='folder_files', blank=True, null=True)
    last_changer = models.ForeignKey(User, null=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(File, self).save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            return reverse('groups:single_folder',kwargs={'slug':self.group.slug, 'pk':self.folder.pk})
        except:
            return reverse('groups:single',kwargs={'slug':self.group.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-uploaded_at']
        unique_together = ['admin','file']
