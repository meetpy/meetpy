from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^meetups$', views.MeetupsListView.as_view(), name='list'),
    url(r'^meetups/(?P<pk>\d+)$', views.MeetupDetailView.as_view(), name='detail'),
    url(r'^meetups/atom/$', views.MeetupsAtomFeed(), name='atom_feed'),
    url(r'^meetups/rss/$', views.MeetupsRssFeed(), name='rss_feed'),
)
