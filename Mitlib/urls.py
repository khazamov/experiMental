from django.conf.urls import patterns, include, url
from django.contrib import admin
from Mitlib import views



urlpatterns = patterns('',
    # Examples:
   
    url(r'^Mitlib/$', views.index, name='index'),
    url(r'^Mitlib/details.html$', views.MyFormView),
    url(r'^post/details.html$', views.MyFormView),

)
