from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify

#from groups.models import Group
#from files.models import Editor, Reader

from django.contrib.auth import get_user_model
User = get_user_model()

class Folder(models.Model):
    name = models.CharField(max_length=128,unique=True)
    group = models.ForeignKey('groups.Group', related_name='group_folders')
    folders =  models.ManyToManyField('self', related_name = 'my_folders', symmetrical=False, blank = True, null = True)
    admin = models.ForeignKey(User, related_name ='folders')

    slug = models.SlugField(allow_unicode=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True,null=True)
    description = models.TextField(blank = True)
    last_changer = models.ForeignKey(User, null=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Folder, self).save(*args, **kwargs)

    def get_absolute_url(self):
        group_slug = self.group.slug
        try:
            for folder in self.object.folders.all():
                return reverse('groups:single_folder',kwargs={'slug':group_slug, 'pk':folder.pk})
        except:
            print "failed"
            return reverse('groups:single',kwargs={'slug':group_slug})

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.name

class FolderMember(models.Model):
    folder = models.ForeignKey(Folder, related_name = 'member_folders')
    user = models.ForeignKey(User, related_name ='folder_members')
    permission = models.CharField(max_length=126, default="reader")
