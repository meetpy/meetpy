from django.contrib.sites.models import Site
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from django.test.utils import override_settings
import factory
from datetime import datetime
from django.test import TestCase
from django.conf import settings
from . import models
from djet import files


class MeetupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Meetup
    FACTORY_DJANGO_GET_OR_CREATE = ('number', 'date')

    number = factory.Sequence(lambda n: n)


class SpeakerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Speaker

    first_name = 'Guido'
    last_name = 'Van Rossum'


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

        self.assertRedirects(response, meetup.get_absolute_url(), status_code=301)

    def test_not_found(self):
        data = {
            'day': '01',
            'month': '02',
            'year': '2000',
        }
        response = self.client.get(reverse('meetups:date_redirect', kwargs=data))

        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)


class SlugifyUploadToTest(TestCase):

    def test_filename(self):
        speaker = SpeakerFactory(first_name='Guido', last_name='Van Rossüm')
        upload_to = models.slugify_upload_to(settings.SPEAKER_PHOTOS_DIR, ['first_name', 'last_name'])

        path = upload_to(speaker, 'bdfl.png')

        self.assertEqual(path, settings.SPEAKER_PHOTOS_DIR + '/guido-van-rossum.png')


class TalkProposalViewTest(TestCase):

    def test_save_talk_proposal_with_existing_speaker(self):
        speaker = SpeakerFactory()
        form_data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'speaker': speaker.id,
        }

        self.client.post(reverse('meetups:talk_proposal'), form_data)

        self.assertEqual(models.Talk.objects.count(), 1)
        saved_talk = models.Talk.objects.all()[0]
        self.assertEqual(saved_talk.title, 'some title')
        self.assertEqual(saved_talk.description, 'some desc')
        self.assertEqual(saved_talk.speakers.count(), 1)
        self.assertEqual(saved_talk.speakers.all()[0], speaker)

    @override_settings(DEFAULT_FILE_STORAGE='djet.files.InMemoryStorage')
    def test_save_talk_proposal_with_new_speaker(self):
        form_data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'speaker_first_name': 'first',
            'speaker_last_name': 'last',
            'speaker_website': 'http://pywaw.org/',
            'speaker_phone': '123',
            'speaker_email': 'email@pywaw.org',
            'speaker_biography': 'short bio',
            'speaker_photo': files.create_inmemory_image('my-pic.png'),
        }

        self.client.post(reverse('meetups:talk_proposal'), form_data)

        self.assertEqual(models.Talk.objects.count(), 1)
        saved_talk = models.Talk.objects.all()[0]
        self.assertEqual(saved_talk.title, 'some title')
        self.assertEqual(saved_talk.description, 'some desc')
        self.assertEqual(saved_talk.speakers.count(), 1)
        saved_speaker = saved_talk.speakers.all()[0]
        self.assertEqual(saved_speaker.first_name, 'first')
        self.assertEqual(saved_speaker.last_name, 'last')
        self.assertEqual(saved_speaker.website, 'http://pywaw.org/')
        self.assertEqual(saved_speaker.phone, '123')
        self.assertEqual(saved_speaker.email, 'email@pywaw.org')
        self.assertEqual(saved_speaker.biography, 'short bio')
        self.assertEqual(saved_speaker.photo.name.split('/')[-1], 'first-last.png')

    @override_settings(TALK_PROPOSAL_RECIPIENTS=['admin1@email.com', 'admin2@email.com'])
    def test_send_email_to_admins(self):
        speaker = SpeakerFactory()
        form_data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'speaker': speaker.id,
        }

        self.client.post(reverse('meetups:talk_proposal'), form_data)

        saved_talk = models.Talk.objects.all()[0]
        context = {
            'talk': saved_talk,
            'site': Site(domain='testserver'),
        }
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            render_to_string('meetups/emails/talk_proposal_subject.txt', context).strip(),
        )
        self.assertEqual(
            mail.outbox[0].body,
            render_to_string('meetups/emails/talk_proposal_body.txt', context),
        )
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].to, settings.TALK_PROPOSAL_RECIPIENTS)
