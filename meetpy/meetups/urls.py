from django.urls import path, re_path
from django.urls import reverse_lazy
from django.views import generic

from . import views

urlpatterns = [
    path('spotkania/', views.MeetupsListView.as_view(), name='meetup_list'),
    re_path(r'^(?P<meetup_type>[\w-]+)/(?P<number>\d+)/$',
        views.MeetupDetailView.as_view(), name='meetup_detail'),
    path('<int:number>/', views.MeetupRedirectOrList.as_view(),
        name='meetup_redirect_or_list'),
    re_path(r'^(?P<meetup_type>[\w-]+)/(?P<number>\d+)/promo/$', views.MeetupPromoView.as_view(), name='meetup_promo'),
    path('sponsorzy/', views.SponsorListView.as_view(), name='sponsor_list'),
    path('prelegenci/', views.SpeakerListView.as_view(), name='speaker_list'),
    path('zgloszenie/', views.TalkProposalCreateView.as_view(), name='talk_proposal'),
    path('zgloszenie/potwierdzenie/', views.TalkProposalConfirmationView.as_view(), name='talk_proposal_confirmation'),
    path('atom/', views.MeetupsAtomFeed(), name='atom_feed'),
    path('rss/', views.MeetupsRssFeed(), name='rss_feed'),

    # Legacy URL's from old website
    path('historia/', generic.RedirectView.as_view(url=reverse_lazy('meetups:meetup_list'), permanent=True)),
    re_path(r'^(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})/$', views.MeetupDateRedirectView.as_view(permanent=True), name='date_redirect'),
    path('home/sponsor/', generic.RedirectView.as_view(url=reverse_lazy('meetups:sponsor_list'), permanent=True)),
    path('home/poradnik-prelegenta', generic.RedirectView.as_view(url=reverse_lazy('meetups:speaker_list'), permanent=True)),
]
