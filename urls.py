from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^Mitlib/', include('Mitlib.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
