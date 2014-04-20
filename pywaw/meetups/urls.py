from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from . import views

urlpatterns = patterns('',
    url(r'^spotkania/$', views.MeetupsListView.as_view(), name='meetup_list'),
    url(r'^(?P<number>\d+)/$', views.MeetupDetailView.as_view(), name='meetup_detail'),
    url(r'^sponsorzy/$', views.SponsorListView.as_view(), name='sponsor_list'),
    url(r'^prelegenci/$', views.SpeakerListView.as_view(), name='speaker_list'),
    url(r'^zgloszenie/$', views.TalkProposalCreateView.as_view(), name='talk_proposal'),
    url(r'^zgloszenie/potwierdzenie/$', views.TalkProposalConfirmationView.as_view(), name='talk_proposal_confirmation'),
    url(r'^atom/$', views.MeetupsAtomFeed(), name='atom_feed'),
    url(r'^rss/$', views.MeetupsRssFeed(), name='rss_feed'),

    # Legacy URL's from old website
    url(r'^historia/$', generic.RedirectView.as_view(url=reverse_lazy('meetups:meetup_list'))),
    url(r'^(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})/$', views.MeetupDateRedirectView.as_view(), name='date_redirect'),
    url(r'^home/sponsor/$', generic.RedirectView.as_view(url=reverse_lazy('meetups:sponsor_list'))),
    url(r'^home/poradnik-prelegenta$', generic.RedirectView.as_view(url=reverse_lazy('meetups:speaker_list'))),
)
