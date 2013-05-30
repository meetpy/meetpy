from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseNotFound
import factory
from datetime import datetime
from django.test import TestCase
from . import models


class MeetupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Meetup
    FACTORY_DJANGO_GET_OR_CREATE = ('name', 'date')

    name = factory.Sequence(lambda n: 'Meetup #{0}'.format(n))


class MeetupManagerTest(TestCase):

    def test_upcoming_if_exists(self):
        previous_meetup = MeetupFactory(date=datetime(2000, 1, 1))
        next_meetup = MeetupFactory(date=datetime(2000, 2, 1))

        upcoming_meetup = models.Meetup.objects.get_upcoming(date=datetime(2000, 1, 15))

        self.assertEqual(next_meetup, upcoming_meetup)

    def test_upcoming_if_not_exists(self):
        with self.assertRaises(models.Meetup.DoesNotExist):
            upcoming_meetup = models.Meetup.objects.get_upcoming(date=datetime(2000, 1, 15))


class MeetupDateRedirectViewTest(TestCase):

    def test_redirect(self):
        data = {
            'day': '01',
            'month': '02',
            'year': '2000',
        }
        meetup = MeetupFactory(date=datetime(2000, 2, 1, 18, 30))

        response = self.client.get(reverse('meetups:date_redirect', kwargs=data))

        self.assertRedirects(response, meetup.get_absolute_url())

    def test_not_found(self):
        data = {
            'day': '01',
            'month': '02',
            'year': '2000',
        }
        response = self.client.get(reverse('meetups:date_redirect', kwargs=data))

        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)
