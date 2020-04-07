# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import auth

# Create your models here.
#class UserData(models.Model):
#    user = models.OneToOneField(User)
    # additional attributes
#    my_groups = models.CharField(max_length=2500, blank= True)
#    waiting_for_approval_groups = models.CharField(max_length = 2500, blank = True)

class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)
