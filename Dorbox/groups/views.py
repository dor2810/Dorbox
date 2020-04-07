# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.urlresolvers import reverse
from django.views import generic

from groups.models import Group, GroupMember, AskedMember
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
User = get_user_model()

from . import models
from . import forms

from django.utils.text import slugify


class GroupMemberList(generic.DetailView,LoginRequiredMixin,generic.edit.FormMixin):
    model = Group
    template_name = "groups/group_members_list.html"
    form_class = forms.PermissionForm

    def get_success_url(self):
        return reverse('groups:members', kwargs={'slug': self.object.slug})


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        try:
            user = User.objects.get(username = username)
        except:
            messages.warning(self.request,'ERROR: user was not found')
            return super(GroupMemberList, self).form_invalid(form)

        permission= form.cleaned_data['permission']
        try:
            gm = GroupMember.objects.get(user = user, group = self.object)
        except:
            messages.warning(self.request,'ERROR: user is not a member of this group')
            return super(GroupMemberList, self).form_invalid(form)
        if (user == self.object.admin):
            messages.warning(self.request,"ERROR: user is the admin. you can't change the admin permission")
            return super(GroupMemberList, self).form_invalid(form)

        gm.permission = permission
        gm.save()
        messages.success(self.request,'SUCCESS: user permission was updated')
        return super(GroupMemberList, self).form_valid(form)



class GroupMemberForm(generic.edit.FormView,LoginRequiredMixin):
    model = Group
    form_class = forms.PermissionForm
    success_url = 'groups:all'

    template_name = "groups/group_members_list.html"

    def form_valid(self, form):
        print "submitted"
        print self.username
        print self.permission
        return super(GroupMemberForm, self).form_valid(form)

        def get_absolute_url(slef, *args, **kwargs):
            return reverse('groups:members',kwargs={'slug':self.kwargs.get('slug')})
        #return reverse('groups:members')

def create_private(request,user_id):

    user = User.objects.get(id=user_id)
    username = user.username

    group_name = request.user.username + " and " + username + " private chat"
    group_slug = slugify(group_name)
    second_slug = username + " and " + request.user.username + " private chat"
    second_slug = slugify(second_slug)

    if Group.objects.filter(slug=second_slug).exists():
        return HttpResponseRedirect(reverse('groups:single',kwargs={'slug':second_slug}))
    elif Group.objects.filter(slug=group_slug).exists():
        return HttpResponseRedirect(reverse('groups:single',kwargs={'slug':group_slug}))


    group = Group.objects.get_or_create(name=group_name,slug=group_slug,admin=request.user, type="private", description="")[0]
    GroupMember.objects.create(user=request.user, group=group)
    GroupMember.objects.create(user=user, group=group)

    return HttpResponseRedirect(reverse('groups:single',kwargs={'slug':group_slug}))

class DeleteGroupMember(LoginRequiredMixin, generic.DeleteView):
    model = GroupMember
    select_related =('admin','group')
#    success_url = reverse('groups:single',kwargs={'slug':object.group.slug})
    template_name="groups/groupmember_confirm_delete.html"

    def get_success_url(self, *args, **kwargs):
        print self.kwargs.get('slug')
        return reverse('groups:members',kwargs={'slug':self.kwargs.get('slug')})

    def get_absolute_url(self, *args, **kwargs):
        print self.kwargs.get('slug')
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
        #return reverse('/')

    def delete(self,*args,**kwargs):
        messages.success(self.request,'GroupMember Deleted')
        return super(DeleteGroupMember, self).delete(*args,**kwargs)

class CreatePrivateChat(LoginRequiredMixin, generic.edit.FormView):
    model = Group
    form_class = forms.CreatePrivateForm
    template_name = "groups/new_private.html"
    success_url = 'groups:all'

    def get_success_url(self):
        return reverse('groups:all')

    def get_queryset(self):
        queryset = super(CreatePrivateChat, self).get_queryset()
        return queryset.filter(admin_id = self.request.user.id)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
    #    self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        description = form.cleaned_data['description']
        try:
            user = User.objects.get(username = username)
        except:
            messages.warning(self.request,'ERROR: user was not found')
            return super(CreatePrivateChat, self).form_invalid(form)

        group_name = self.request.user.username + " and " + username + " private chat"
        group_slug = slugify(group_name)
        second_slug = username + " and " + self.request.user.username + " private chat"
        second_slug = slugify(second_slug)

        if Group.objects.filter(slug=second_slug).exists() or Group.objects.filter(slug=group_slug).exists():
            msg = "Error: " + username + " and you are already in a private chat!"
            messages.warning(self.request, msg)
            return super(CreatePrivateChat, self).form_invalid(form)

        group = Group.objects.get_or_create(name=group_name,slug=group_slug,admin=self.request.user, type="private", description=description)[0]

        GroupMember.objects.create(user=self.request.user, group=group)
        GroupMember.objects.create(user=user, group=group)

        msg = "SUCCESS: you created a private chat to " + username + " and you"
        messages.success(self.request, msg)
        return super(CreatePrivateChat, self).form_valid(form)


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group

    def get_absolute_url(slef, *args, **kwargs):
        #return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
        return reverse('groups:all')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        group = self.object
        group.admin = self.request.user
        self.object.save()

        #print User.objects.get(username="dordordor12")
        try:
            GroupMember.objects.get_or_create(user=self.request.user,group=group, permission="admin")
        except:
            messages.warning(self.request,'Warning already a member!')
            print "failed"
        else:
            messages.success(self.request,'You are now a member!')
            print "success"

        return super(CreateGroup, self).form_valid(form)

class CreateNewAskedMember(LoginRequiredMixin, generic.CreateView):
    fields = ('username',)
    model = AskedMember
    template_name = "groups/invite_new_member.html"



    def get_absolute_url(slef, *args, **kwargs):

        return reverse('groups:single',kwargs={'slug':my_slug})

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:all')



    def form_valid(self, form):

        self.object = form.save(commit=False)


        my_slug = self.kwargs['slug']
        try:
            self.object.user = User.objects.get(username=self.object.username)
        except:
            print "failed user"
            err_msg = "ERROR: username " + str(self.object.username) + " wasn't found!"
            messages.error(self.request,err_msg)
            return super(CreateNewAskedMember, self).form_invalid(form)
        else:
            print "success user"

        try:
            group = Group.objects.get(slug=my_slug)
            self.object.group = group
        except:
            print "failed group"
            return super(CreateNewAskedMember, self).form_invalid(form)
        else:
            print "success group"

        if self.object.user.group_set.filter(slug=my_slug).exists(): # checks if a user is already in the group
            err_msg = "ERROR: username " + str(self.object.username) + " is already in the group"
            messages.error(self.request,err_msg)
            return super(CreateNewAskedMember, self).form_invalid(form)

        self.object.save()
        return super(CreateNewAskedMember, self).form_valid(form)


class SingleGroup(generic.DetailView, LoginRequiredMixin):
    model = Group

class ListGroups(generic.ListView,LoginRequiredMixin):
    model = Group
    template_name = "groups/group_list.html"

class ListPrivateChats(generic.ListView,LoginRequiredMixin):
    model = Group
    template_name = "groups/private_list.html"

class ListPendingsGroup(generic.ListView,LoginRequiredMixin):
    model = Group
    template_name = "groups/pending_groups_list.html"

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request,'You are now a member!')

        AskedMember.objects.filter(user= self.request.user, group = group).delete()

        return super(JoinGroup, self).get(request, *args,**kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:all')

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExsit:
            messages.warning(self.request,'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request,'You are no longer a member of this group!')
        return super(LeaveGroup, self).get(request, *args,**kwargs)
