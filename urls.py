from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^Mitlib/', include('Mitlib.urls', namespace = "Mitlib")),
    url(r'^admin/', include(admin.site.urls)),
)
