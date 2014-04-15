from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.syndication import views as syndication_views
from django.core.urlresolvers import reverse_lazy
from django.utils import feedgenerator
from . import models, forms, constants


class MeetupsListView(generic.ListView):
    model = models.Meetup


class MeetupDetailView(generic.DetailView):
    model = models.Meetup
    slug_url_kwarg = slug_field = 'number'


class MeetupDateRedirectView(generic.RedirectView):

    def get_redirect_url(self, **kwargs):
        date_lookup = {'date__' + k: v for k, v in kwargs.items()}
        meetup = get_object_or_404(models.Meetup, **date_lookup)
        return meetup.get_absolute_url()


class MeetupsRssFeed(syndication_views.Feed):
    title = constants.FEED_TITLE
    link = reverse_lazy('meetups:meetup_list')
    title_template = models.Meetup._meta.app_label + '/feed/meetup_title.txt'
    description_template = models.Meetup._meta.app_label + '/feed/meetup_description.html'

    def items(self):
        return models.Meetup.objects.filter(is_ready=True)

    def item_pubdate(self, item):
        return item.date_modified


class MeetupsAtomFeed(MeetupsRssFeed):
    feed_type = feedgenerator.Atom1Feed


class SponsorListView(generic.ListView):
    model = models.Sponsor


class SpeakerListView(generic.ListView):
    model = models.Speaker


class TalkProposalView(generic.FormView):
    form_class = forms.TalkProposalForm
    template_name = 'meetups/talk_proposal.html'

    def form_valid(self, form):
        created_talk = models.Talk.objects.create(title=form.cleaned_data['talk_title'],
                                                  description=form.cleaned_data['talk_description'])
        if form.cleaned_data['speaker']:
            added_speaker = form.cleaned_data['speaker']
        else:
            added_speaker = models.Speaker.objects.create(first_name=form.cleaned_data['speaker_first_name'],
                                                          last_name=form.cleaned_data['speaker_last_name'],
                                                          website=form.cleaned_data['speaker_website'],
                                                          phone=form.cleaned_data['speaker_phone'],
                                                          email=form.cleaned_data['speaker_email'],
                                                          biography=form.cleaned_data['speaker_biography'],
                                                          photo=form.cleaned_data['speaker_photo'])
        created_talk.speakers.add(added_speaker)
        return redirect('meetups:meetup_list')
