import datetime

from django.views import generic

from meetups import models as meetups_models
from . import models


class HomeView(generic.TemplateView):
    template_name = 'misc/home.html'

    def get_context_data(self):
        context = super().get_context_data()
        today = datetime.date.today()
        try:
            context['upcoming_meetup'] = meetups_models.Meetup.objects.get_upcoming(today)
        except meetups_models.Meetup.DoesNotExist:
            context['upcoming_meetup'] = None
        context['partners'] = models.Partner.objects.filter(is_public=True)
        context["previous_meetups"] = meetups_models.Meetup.objects.past(today)[:3]
        return context


class FaqView(generic.TemplateView):
    template_name = 'misc/faq.html'
