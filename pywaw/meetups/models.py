from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to=settings.SPONSOR_LOGOS_DIR)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class MeetupManager(models.Manager):

    def get_upcoming(self, date=None):
        date = date or datetime.now()
        try:
            return self.filter(date__gte=date).order_by('date')[0]
        except IndexError:
            raise self.model.DoesNotExist


class Meetup(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    sponsors = models.ManyToManyField(Sponsor, related_name='sponsored_meetups')
    venue = models.ForeignKey(Venue, related_name='meetups', null=True, blank=True)
    is_ready = models.BooleanField()

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
    photo = models.ImageField(upload_to=settings.SPEAKER_PHOTOS_DIR)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Talk(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    speakers = models.ManyToManyField(Speaker, related_name='talks')
    meetup = models.ForeignKey(Meetup, related_name='talks')
    time = models.TimeField()

    class Meta:
        ordering = ['time']

    def __str__(self):
        return '{} ({})'.format(self.title, self.meetup)


class Photo(models.Model):
    meetup = models.ForeignKey(Meetup, related_name='photos')
    image = models.ImageField(upload_to=settings.MEETUP_PHOTOS_DIR)

