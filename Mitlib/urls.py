from django.conf.urls import patterns, include, url
from django.contrib import admin
from Mitlib import views



urlpatterns = patterns('',
    # Examples:
   
    url(r'^Mitlib/$', views.index, name='index'),
    url(r'^Mitlib/(?P<question_id>\d+)', views.detail, name  = 'detail'),
    url(r'^Mitlib/(?P<question_id>\d+)/results$', views.results, name = 'results'),
    url(r'^Mitlib/(?P<vote_id>\d+)/votes$', views.votes,name = 'votes'),

)
