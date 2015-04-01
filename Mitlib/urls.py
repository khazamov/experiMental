from django.conf.urls import patterns, include, url
from django.contrib import admin
from Mitlib import views



urlpatterns = patterns('',

    url(r'^Mitlib/$', views.index, name='index'),
    url(r'^Mitlib/(?P<pk>\d+)/', views.DetailView.as_view(), name  = 'detail'),
    url(r'^Mitlib/(?P<question_id>\d+)/result/$', views.result, name = 'result'),
    url(r'^Mitlib/(?P<question_id>\d+)/votes$', views.votes, name = 'vote'),
    url(r'^Mitlib/traderesult\d?$', views.traderesult, name = 'traderesult')


)
