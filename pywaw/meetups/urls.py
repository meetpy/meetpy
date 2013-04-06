from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^meetups$', views.MeetupsListView.as_view(), name='list'),
    url(r'^meetups/(?P<pk>\d+)$', views.MeetupDetailView.as_view(), name='detail'),
)
