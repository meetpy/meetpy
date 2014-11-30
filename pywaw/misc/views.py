from django.views import generic
from meetups import models as meetups_models
from . import models


class HomeView(generic.TemplateView):
    template_name = 'misc/home.html'

    def get_context_data(self):
        context = super().get_context_data()
        try:
            context['upcoming_meetup'] = meetups_models.Meetup.objects.get_upcoming()
        except meetups_models.Meetup.DoesNotExist:
            context['upcoming_meetup'] = None
        context['partners'] = models.Partner.objects.filter(is_public=True)
        return context
