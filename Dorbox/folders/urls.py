from django.conf.urls import url

from . import views

app_name = 'folders'
urlpatterns =[
    url(r"delete/(?P<pk>\d+)/$", views.DeleteFolder.as_view(),name='delete'),
    url(r'^new/',views.CreateFolder.as_view(),name='create'),
    url(r'^in/(?P<slug1>[-\w]+)/(?P<pk>\d+)/$',views.SingleFolder.as_view(), name='single'),

#url(r'^in/download-folder/(?P<path>.*)$', views.download, name='download'),
    #url(r'^new/dor/',views.create_file,name='c'),
]
