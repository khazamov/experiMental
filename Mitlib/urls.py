from django.conf.urls import patterns, include, url
from django.contrib import admin
from Mitlib import views



urlpatterns = patterns('',
    # Examples:
   
    url(r'^Mitlib/$', views.index, name='index'),
    url(r'^Mitlib/(?P<question_id>\d+)', views.detail, name  = 'detail'),
    url(r'^Mitlib/(?P<question_id>\d+)/result$', views.result, name = 'result'),
    url(r'^Mitlib/(?P<question_id>\d+)/votes$', views.votes,name = 'votes'),
    url(r'^Mitlib/polls/index.html$', views.index,name = 'index'),


)
