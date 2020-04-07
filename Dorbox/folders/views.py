# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from django.views import generic
from django.http import HttpResponse,Http404

from django.contrib import messages

from braces.views import SelectRelatedMixin

import os
from django.conf import settings

from django.utils.text import slugify

from . import models
from . import forms
from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

class SingleFolder(generic.DetailView, LoginRequiredMixin):
    model = models.Folder
    template_name = "folders/folder_detail.html"

class CreateFolder(LoginRequiredMixin, generic.CreateView):

    fields = ('name','description')
    model = models.Folder
    template_name = "folders/folder_form.html"

    def get_success_url(self, *args, **kwargs):
        try:
            return reverse('groups:single_folder',kwargs={'slug':self.kwargs['slug'], 'pk':self.kwargs['pk']})
        except:
            return reverse('groups:single',kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.admin = self.request.user
        self.object.slug = slugify(self.object.name)

        group_slug = self.kwargs['slug']
        group = Group.objects.get(slug=group_slug)
        self.object.group = group
        try:
            parent_folder = models.Folder.objects.get(pk=self.kwargs['pk'])# when we are in the group_details, not uder a folder this will fail
            self.object.save()
            self.object.folders.add(parent_folder)
        except:
            pass
        self.object.save()

        return super(CreateFolder, self).form_valid(form)

class DeleteFolder(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Folder
    select_related =('admin','group')
#    success_url =reverse_lazy('groups:all')
    template_name="folders/folder_confirm_delete.html"

    def delete(self,*args,**kwargs):
        c = 0
        try:
            print models.Folder.objects.get(pk=self.kwargs['pk']).name
            my_folder = models.Folder.objects.get(pk=self.kwargs['pk'])
            for folder in my_folder.folders.all():
                c += 1
                self.success_url =  reverse('groups:single_folder',kwargs={'slug':self.kwargs['slug'],'pk':folder.pk})
        except:
            self.success_url =  reverse('groups:single',kwargs={'slug':self.kwargs['slug']})

        if c == 0:
            self.success_url =  reverse('groups:single',kwargs={'slug':self.kwargs['slug']})

        return super(DeleteFolder, self).delete(*args,**kwargs)

class UpdateFolder(LoginRequiredMixin, SelectRelatedMixin, generic.UpdateView):
    model = models.Folder
    template_name = "folders/update_folder.html"
    select_related = ('admin',)
    form_class = forms.UpdateForm

    def get_success_url(self, *args, **kwargs):
        group_slug = self.kwargs['slug']
        try:
            for folder in self.object.folders.all():
                return reverse('groups:single_folder',kwargs={'slug':group_slug, 'pk':folder.pk})
        except:
            return reverse('groups:single',kwargs={'slug':group_slug})

    # def get_form_kwargs(self):
    #     kwargs = super(UpdateFolder, self).get_form_kwargs()
    #     kwargs['slug'] = self.kwargs['slug']
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.folders.clear()
        try:
            pass
        except:
            print "failed"

    #    new_parent = (form.cleaned_data['folders']).objects.all()
    #    self.object.folders.add(new_parent)

        self.object.name = form.cleaned_data['name']
        self.object.description = form.cleaned_data['description']
        self.object.save()
        self.object.slug = slugify(self.object.name)
        self.object.last_changer = self.request.user
        self.object.save()

        return super(UpdateFolder, self).form_valid(form)

    def form_invalid(self,form):
        print "invalid?"
        return super(UpdateFolder, self).form_invalid(form)
