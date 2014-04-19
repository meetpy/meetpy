from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.syndication import views as syndication_views
from django.core.urlresolvers import reverse_lazy
from django.utils import feedgenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
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
    success_url = reverse_lazy('meetups:talk_proposal_confirmation')

    def form_valid(self, form):
        talk = self._create_talk_and_speaker(form.cleaned_data)
        self._send_email_to_admins(talk)
        return super().form_valid(form)

    def _create_talk_and_speaker(self, data):
        created_talk = models.Talk.objects.create(
            title=data['talk_title'],
            description=data['talk_description'],
        )
        if data['speaker']:
            added_speaker = data['speaker']
        else:
            added_speaker = models.Speaker.objects.create(
                first_name=data['speaker_first_name'],
                last_name=data['speaker_last_name'],
                website=data['speaker_website'],
                phone=data['speaker_phone'],
                email=data['speaker_email'],
                biography=data['speaker_biography'],
                photo=data['speaker_photo'],
            )
        created_talk.speakers.add(added_speaker)
        return created_talk

    def _send_email_to_admins(self, talk):
        context = {
            'talk': talk,
            'site': get_current_site(self.request),
        }
        send_mail(
            subject=render_to_string('meetups/emails/talk_proposal_subject.txt', context).strip(),
            message=render_to_string('meetups/emails/talk_proposal_body.txt', context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.TALK_PROPOSAL_RECIPIENTS,
        )


class TalkProposalConfirmationView(generic.TemplateView):
    template_name = 'meetups/talk_proposal_confirmation.html'
