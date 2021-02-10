from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication import views as syndication_views
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils import feedgenerator
from django.views import generic

from django.db.models import Q
from itertools import chain

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
        self._send_email_to_admins()
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


class TalkProposalConfirmationView(generic.TemplateView):
    template_name = 'meetups/talkproposal_confirmation.html'


class SearchView(generic.TemplateView):
    template_name='meetups/search_results.html'

    def search(self):
        query = self.request.GET.get('q')
        talks = models.Talk.objects.filter(Q(description__icontains=query) | Q(title__contains=query))
        events = models.Meetup.objects.filter(Q(description__icontains=query))
        speakers = models.Speaker.objects.filter(Q(biography__icontains=query))
        results = chain(talks, events, speakers)
        return results

    def get_context_data(self):
        search = self.search()
        return {
            'search': search,
        }





