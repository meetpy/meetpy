from . import models
from datetime import datetime


def stats(request):
    now = datetime.now()
    return {
        'meetups_stats': {
            'meetups_count': models.Meetup.objects.filter(date__lt=now).count(),
            'talks_count': models.Talk.objects.filter(meetup__date__lt=now).count(),
            'speakers_count': models.Speaker.objects.filter(talks__meetup__date__lt=now).distinct().count(),
        }
    }
