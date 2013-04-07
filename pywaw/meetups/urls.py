from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.MeetupsListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.MeetupDetailView.as_view(), name='detail'),
    url(r'^atom/$', views.MeetupsAtomFeed(), name='atom_feed'),
    url(r'^rss/$', views.MeetupsRssFeed(), name='rss_feed'),
)
