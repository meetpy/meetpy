from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^historia/$', views.MeetupsListView.as_view(), name='meetup_list'),
    url(r'^(?P<number>\d+)/$', views.MeetupDetailView.as_view(), name='meetup_detail'),
    url(r'^(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})/$', views.MeetupDateRedirectView.as_view(),
        name='date_redirect'),
    url(r'^sponsor/$', views.SponsorListView.as_view(), name='sponsor_list'),
    url(r'^atom/$', views.MeetupsAtomFeed(), name='atom_feed'),
    url(r'^rss/$', views.MeetupsRssFeed(), name='rss_feed'),
)
