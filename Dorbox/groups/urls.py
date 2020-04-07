from django.conf.urls import url
from . import views
from files import views as file_views
from folders import views as folder_views

app_name = "groups"

urlpatterns =[
    url(r'^private-chats/$',views.ListPrivateChats.as_view(),name ='private'),
    url(r'^$',views.ListGroups.as_view(),name ='all'),
    url(r'^new-private/$',views.CreatePrivateChat.as_view(),name='create-private'),
    url(r'^new/$',views.CreateGroup.as_view(),name='create'),
    url(r'^new-private/(?P<user_id>\d+)/$',views.create_private,name='create-private-username'),
    url(r'^in/(?P<slug>[-\w]+)/$',views.SingleGroup.as_view(), name='single'),
    url(r"join/(?P<slug>[-\w]+)/$", views.JoinGroup.as_view(),name='join'),
    url(r"leave/(?P<slug>[-\w]+)/$", views.LeaveGroup.as_view(),name='leave'),
    url(r'^pendings',views.ListPendingsGroup.as_view(),name='pending'),
    url(r"^(?P<slug>[-\w]+)/invite-new-member/$", views.CreateNewAskedMember.as_view(),name='invite_member'),
    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/confirm-delete-member/$',views.DeleteGroupMember.as_view(),name='delete_member'),

    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/new-file/$',file_views.CreateFile.as_view(),name='create_file'),
    url(r'^in/(?P<slug>[-\w]+)/new-file/$',file_views.CreateFile.as_view(),name='create_file'),
    url(r'^in/(?P<slug>[-\w]+)/(?P<folder_pk>\d+)/(?P<pk>\d+)/confirm-delete-file/$',file_views.DeleteFile.as_view(),name='delete_file'),
    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/confirm-delete-file/$',file_views.DeleteFile.as_view(),name='delete_file'),
    url(r'^in/(?P<slug>[-\w]+)/group-members/$',views.GroupMemberList.as_view(),name='members'),
    url(r'^in/(?P<slug>[-\w]+)/edit-permission/$',views.GroupMemberForm.as_view(),name='edit_permission'),
    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/edit-file/$',file_views.UpdateFile.as_view(),name='edit_file'),

    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/download-folder/$',file_views.download_folder ,name='download_folder'),
    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/new-folder/$',folder_views.CreateFolder.as_view(),name='create_folder'),
    url(r'^in/(?P<slug>[-\w]+)/new-folder/$',folder_views.CreateFolder.as_view(),name='create_folder'),
    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/edit-folder/$',folder_views.UpdateFolder.as_view(),name='edit_folder'),
    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/confirm-delete-folder/$',folder_views.DeleteFolder.as_view(),name='delete_folder'),
    url(r'^in/(?P<slug>[-\w]+)/(?P<pk>\d+)/in-folder/$',folder_views.SingleFolder.as_view(),name='single_folder'),
]
