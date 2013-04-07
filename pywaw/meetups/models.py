from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class MeetupManager(models.Manager):

    def get_upcomming(self, date):
        try:
            return self.filter(date__gte=date).order_by('date')[0]
        except IndexError:
            raise self.model.DoesNotExist



class Meetup(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()

    objects = MeetupManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('meetups:detail', kwargs={'pk': self.id})


class Speaker(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    website = models.URLField(blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Talk(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    speaker = models.ForeignKey(Speaker, related_name='speakers')
    meetup = models.ForeignKey(Meetup, related_name='talks')
    time = models.TimeField()

    class Meta:
        ordering = ['time']

    def __str__(self):
        return '{} - {}'.format(self.title, self.speaker)


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to=settings.SPONSOR_LOGOS_DIR)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Sponsorship(models.Model):
    sponsor = models.ForeignKey(Sponsor)
    meetup = models.ForeignKey(Meetup)

    def __str__(self):
        return '{} - {}'.format(self.meetup, self.sponsor)
