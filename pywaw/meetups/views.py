from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.syndication import views as syndication_views
from django.core.urlresolvers import reverse_lazy
from django.utils import feedgenerator
from . import models, constants


class MeetupsListView(generic.ListView):
    model = models.Meetup


class MeetupDetailView(generic.DetailView):
    model = models.Meetup
    slug_url_kwarg = slug_field = 'number'


class MeetupDateRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        date_lookup = {'date__' + k: v for k, v in kwargs.items()}
        meetup = get_object_or_404(models.Meetup, **date_lookup)
        return meetup.get_absolute_url()


class MeetupsRssFeed(syndication_views.Feed):
    title = constants.FEED_TITLE
    link = reverse_lazy('meetups:list')
    title_template = models.Meetup._meta.app_label + '/feed/meetup_title.txt'
    description_template = models.Meetup._meta.app_label + '/feed/meetup_description.html'

    def items(self):
        return models.Meetup.objects.filter(is_ready=True)


class MeetupsAtomFeed(MeetupsRssFeed):
    feed_type = feedgenerator.Atom1Feed


class SponsorListView(generic.ListView):
    model = models.Sponsor


class SpeakerListView(generic.ListView):
    model = models.Speaker
