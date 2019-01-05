from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.create_education, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^registerCompany/$', views.registerCompany, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^create/$', views.create_education, name='create'),
        url(r'^create/edit/(?P<id>\d+)$', views.edit, name='edit'),
        url(r'^create/edit/update/(?P<id>\d+)$', views.update, name='update'),
        url(r'^create/delete/(?P<id>\d+)$', views.delete, name='delete'),
        url(r'^logout/$', views.user_logout, name='logout'),

    ]
