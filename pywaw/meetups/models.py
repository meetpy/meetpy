from django.db import models
from django.core.urlresolvers import reverse


class Meetup(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()

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
