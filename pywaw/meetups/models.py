from django.db import models
from django.core.urlresolvers import reverse


class Meetup(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('meetups:detail', kwargs={'pk': self.id})
