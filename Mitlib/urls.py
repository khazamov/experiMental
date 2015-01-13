from django.conf.urls import patterns, include, url
from django.contrib import admin
from Mitlib import views



urlpatterns = patterns('',
    # Examples:
   
    url(r'^Mitlib/$', views.IndexView.as_view(), name='index'),
    url(r'^Mitlib/(?P<pk>\d+)/', views.DetailView.as_view(), name  = 'detail'),
    url(r'^Mitlib/(?P<pk>\d+)/result$', views.ResultView.as_view(), name = 'result'),
    url(r'^Mitlib/(?P<question_id>\d+)/votes$', views.votes, name = 'votes'),



)
