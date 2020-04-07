# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse

from django.views import generic
from django.http import HttpResponse,Http404

from django.contrib import messages

from braces.views import SelectRelatedMixin

import os
from django.conf import settings

from django.utils.text import slugify
from folders.models import Folder
from groups.models import Group
from . import models
from . import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()


def create_file(request):
    print "inside create_file func"
    if request.method == 'POST':
        print "inside post"
        uploaded_file = request.FILES['document']
        print uploaded_file.name
        return render(request,"index.html")

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def download_folder(request, slug, pk):
    folder = Folder.objects.get(pk = pk)
    for file in folder.folder_files.all():
        download(request,file.file)
    return HttpResponseRedirect(reverse('groups:single_folder',kwargs={'slug':slug,'pk':pk}))

class SingleFile(generic.DetailView, LoginRequiredMixin):
    model = models.File

class CreateFile(LoginRequiredMixin, generic.CreateView):
    fields = ('name','file','description')
    model = models.File

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.admin = self.request.user
        try:
            folder = Folder.objects.get(pk=self.kwargs['pk'])
            print " file inside " + folder.name
            self.object.folder = folder
        except:
            print "file is not in a folder"

        group = Group.objects.get(slug=self.kwargs['slug'])
        self.object.group = group

        self.object.save()

        return super(CreateFile, self).form_valid(form)

class DeleteFile(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.File
    select_related =('admin','group')
    success_url =reverse_lazy('groups:all')
    template_name="files/file_confirm_delete.html"

    def get_absolute_url(slef, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
        #return reverse('/')


    def delete(self,*args,**kwargs):
        try:
            my_folder = Folder.objects.get(pk=self.kwargs['folder_pk'])
            self.success_url =  reverse('groups:single_folder',kwargs={'slug':self.kwargs['slug'],'pk':my_folder.pk})
        except:
            self.success_url =  reverse('groups:single',kwargs={'slug':self.kwargs['slug']})


        return super(DeleteFile, self).delete(*args,**kwargs)

class UpdateFile(LoginRequiredMixin, SelectRelatedMixin, generic.UpdateView):
    model = models.File
    template_name = "files/update_file.html"
    select_related = ('admin',)
    form_class = forms.UpdateForm

    def get_form_kwargs(self):
        kwargs = super(UpdateFile, self).get_form_kwargs()
        kwargs['slug'] = self.kwargs['slug']
        print kwargs['slug']
        return kwargs

    def get_success_url(self, *args, **kwars):
        try:
            return reverse('groups:single_folder',kwargs={'slug':self.kwargs['slug'], 'pk':self.object.folder.pk})
        except:
            return reverse('groups:single',kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.folder = form.cleaned_data['folder']
        self.object.name = form.cleaned_data['name']
        self.object.description = form.cleaned_data['description']
        self.object.slug = slugify(self.object.name)
        self.object.last_changer = self.request.user

        self.object.save()

        return super(UpdateFile, self).form_valid(form)
