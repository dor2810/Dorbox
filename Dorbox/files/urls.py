from django.conf.urls import url

from . import views

app_name = 'files'
urlpatterns =[
#    url(r'new/$',views.CreateFile.as_view(), name='create'),
    url(r"delete/(?P<pk>\d+)/$", views.DeleteFile.as_view(),name='delete'),
    url(r'^new/',views.CreateFile.as_view(),name='create'),
    url(r'^in/(?P<slug>[-\w]+)/file/$',views.SingleFile.as_view(), name='single'),
    url(r'^in/download-file/(?P<path>.*)$', views.download, name='download'),
    url(r'^new/dor/',views.create_file,name='create_file'),
]
