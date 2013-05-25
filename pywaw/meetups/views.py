from django.views import generic
from django.contrib.syndication import views as syndication_views
from django.core.urlresolvers import reverse_lazy
from django.utils import feedgenerator
from . import models, constants


class MeetupsListView(generic.ListView):
    model = models.Meetup


class MeetupDetailView(generic.DetailView):
    model = models.Meetup


class MeetupsRssFeed(syndication_views.Feed):
    title = constants.FEED_TITLE
    link = reverse_lazy('meetups:list')
    title_template = models.Meetup._meta.app_label + '/feed/meetup_title.txt'
    description_template = models.Meetup._meta.app_label + '/feed/meetup_description.html'

    def items(self):
        return models.Meetup.objects.filter(is_ready=True)


class MeetupsAtomFeed(MeetupsRssFeed):
    feed_type = feedgenerator.Atom1Feed
