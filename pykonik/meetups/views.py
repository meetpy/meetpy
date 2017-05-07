from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
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


class MeetupPromoView(generic.DetailView):
    model = models.Meetup
    slug_url_kwarg = slug_field = 'number'
    template_name = 'meetups/meetup_promo.html'


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

    def get_queryset(self):
        return super().get_queryset().filter(talks__meetup__isnull=False).distinct()


class TalkProposalCreateView(generic.CreateView):
    model = models.TalkProposal
    form_class = forms.TalkProposalForm
    success_url = reverse_lazy('meetups:talk_proposal_confirmation')

    def form_valid(self, form):
        response = super().form_valid(form)
        self._send_email_to_admins()
        return response

    def _send_email_to_admins(self):
        context = {
            'talk_proposal': self.object,
            'site': get_current_site(self.request),
        }
        send_mail(
            subject=render_to_string('meetups/emails/talk_proposal_subject.txt', context).strip(),
            message=render_to_string('meetups/emails/talk_proposal_body.txt', context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.TALK_PROPOSAL_RECIPIENTS,
        )


class TalkProposalConfirmationView(generic.TemplateView):
    template_name = 'meetups/talkproposal_confirmation.html'
