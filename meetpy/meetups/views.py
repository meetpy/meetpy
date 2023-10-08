import logging

from discord_webhook import DiscordEmbed, DiscordWebhook
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication import views as syndication_views
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils import feedgenerator
from django.views import generic

from . import models, forms


class MeetupsListView(generic.ListView):
    model = models.Meetup


class MeetupRedirectOrList(generic.View):
    """
    Redirects if possible, if not then displays list of matching Meetups
    """

    template_name = "meetups/meetup_list.html"

    def get(self, request, **kwargs):
        number = self.kwargs['number']

        meetups = models.Meetup.objects.filter(number=number)
        if len(meetups) == 0:
            raise Http404

        if len(meetups) == 1:
            return redirect(meetups[0].get_absolute_url())

        return TemplateResponse(
            request,
            self.template_name,
            {'object_list': meetups}
        )


class MeetupDetailView(generic.TemplateView):

    template_name = 'meetups/meetup_detail.html'

    def get_object(self):
        lookup = {
            'meetup_type__slug': self.kwargs['meetup_type'],
            'number': self.kwargs['number'],
        }
        return get_object_or_404(models.Meetup, **lookup)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['meetup'] = self.get_object()
        return ctx


class MeetupPromoView(generic.TemplateView):
    model = models.Meetup
    slug_url_kwarg = slug_field = 'number'
    template_name = 'meetups/meetup_promo.html'

    def get_object(self):
        lookup = {
            'meetup_type__slug': self.kwargs['meetup_type'],
            'number': self.kwargs['number'],
        }
        return get_object_or_404(models.Meetup, **lookup)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        meetup = self.get_object()
        ctx['meetup'] = meetup
        ctx['meetup_url'] = self.request.build_absolute_uri(meetup.get_absolute_url())
        return ctx


class MeetupDateRedirectView(generic.RedirectView):

    def get_redirect_url(self, **kwargs):
        date_lookup = {'date__' + k: v for k, v in kwargs.items()}
        meetup = get_object_or_404(models.Meetup, **date_lookup)
        return meetup.get_absolute_url()


class MeetupsRssFeed(syndication_views.Feed):
    title = settings.CONSTANT['FEED_TITLE']
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
        try:
            self._send_email_to_admins()
        except Exception:
            logging.exception("Couldn't send email to admins about the new talk proposal")
            pass
        try:
            self._send_message_on_discord()
        except Exception:
            logging.exception("Couldn't send a message on discord")
            pass
        return response

    def _send_email_to_admins(self):
        context = {
            'talk_proposal': self.object,
            'site': get_current_site(self.request),
            'page_address': settings.CONSTANT['GROUP_PAGE_ADDRESS_SHORT'],
        }
        send_mail(
            subject=render_to_string('meetups/emails/talk_proposal_subject.txt', context).strip(),
            message=render_to_string('meetups/emails/talk_proposal_body.txt', context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.TALK_PROPOSAL_RECIPIENTS,
        )

    def _send_message_on_discord(self):
        proposal: models.TalkProposal = self.object
        if settings.DISCORD_FORM_WEBHOOK_URL is None:
            return
        webhook = DiscordWebhook(
            username="Talk Proposal Announcer",
            url=settings.DISCORD_FORM_WEBHOOK_URL,
            content="A new proposal has been submitted",
        )

        language_emoji = "🇵🇱" if proposal.talk.language == "pl" else "🇬🇧"

        talk_embed = DiscordEmbed(
            title=f"{language_emoji} {proposal.talk.title}",
            description=proposal.talk.description,
            url=self.request.build_absolute_uri(
                reverse("admin:meetups_talk_change", args=(proposal.talk_id,))
            ),
            color=0x3A76A6,
            timestamp=proposal.date_submitted,
        )
        webhook.add_embed(talk_embed)

        if speaker := proposal.talk.speakers.first():
            talk_embed.set_author(
                name=str(speaker),
                icon_url=self.request.build_absolute_uri(speaker.photo.url),
            )
            speaker_embed = DiscordEmbed(
                title="About speaker",
                description=speaker.biography,
                color=0xFFD847,
                thumbnail=self.request.build_absolute_uri(speaker.photo.url),
            )
            if speaker.phone:
                speaker_embed.add_embed_field(name="Phone", value=speaker.phone)
            if speaker.website:
                speaker_embed.add_embed_field(name="Website", value=speaker.website)
            if speaker.email:
                speaker_embed.add_embed_field(name="Email", value=speaker.email)
            if speaker.discord_handle:
                speaker_embed.add_embed_field(name="Discord", value=speaker.discord_handle)
            if speaker.slack_handle:
                speaker_embed.add_embed_field(name="Slack", value=speaker.slack_handle)
            webhook.add_embed(speaker_embed)

        if proposal.message:
            message_embed = DiscordEmbed(
                title="Additional comments",
                description=proposal.message,
                color=0x616161,
            )
            webhook.add_embed(message_embed)

        webhook.execute()


class TalkProposalConfirmationView(generic.TemplateView):
    template_name = 'meetups/talkproposal_confirmation.html'
