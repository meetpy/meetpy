from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('misc.urls', namespace='misc')),
    url(r'^', include('meetups.urls', namespace='meetups')),
    url(r'^admin/', include(admin.site.urls)),
)
