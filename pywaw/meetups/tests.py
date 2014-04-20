from django.contrib.sites.models import get_current_site
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.loader import render_to_string
from django.test.utils import override_settings
import factory
from datetime import datetime
from django.test import TestCase
from django.conf import settings
from djet import files, testcases, assertions
from . import models, views


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


class MeetupDateRedirectViewTest(testcases.ViewTestCase, assertions.StatusCodeAssertionsMixin):
    view_class = views.MeetupDateRedirectView

    def test_redirect(self):
        data = {
            'day': '01',
            'month': '02',
            'year': '2000',
        }
        meetup = MeetupFactory(date=datetime(2000, 2, 1, 18, 30))
        request = self.factory.get(data=data)

        response = self.view(request)

        self.assert_redirect(response, meetup.get_absolute_url())

    def test_not_found(self):
        data = {
            'day': '01',
            'month': '02',
            'year': '2000',
        }
        request = self.factory.get(data=data)

        with self.assertRaises(Http404):
            self.view(request)


class SlugifyUploadToTest(TestCase):

    def test_filename(self):
        speaker = SpeakerFactory(first_name='Guido', last_name='Van Rossüm')
        upload_to = models.slugify_upload_to(settings.SPEAKER_PHOTOS_DIR, ['first_name', 'last_name'])

        path = upload_to(speaker, 'bdfl.png')

        self.assertEqual(path, settings.SPEAKER_PHOTOS_DIR + '/guido-van-rossum.png')


class TalkProposalViewTest(testcases.ViewTestCase, assertions.StatusCodeAssertionsMixin):
    view_class = views.TalkProposalView

    def test_save_talk_proposal_with_existing_speaker(self):
        speaker = SpeakerFactory()
        data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'speaker': speaker.id,
        }
        request = self.factory.post(data=data)

        self.view(request)

        self.assertEqual(models.Talk.objects.count(), 1)
        saved_talk = models.Talk.objects.all()[0]
        self.assertEqual(saved_talk.title, data['talk_title'])
        self.assertEqual(saved_talk.description, data['talk_description'])
        self.assertEqual(saved_talk.speakers.count(), 1)
        self.assertEqual(saved_talk.speakers.all()[0], speaker)

    @override_settings(DEFAULT_FILE_STORAGE='djet.files.InMemoryStorage')
    def test_save_talk_proposal_with_new_speaker(self):
        data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'speaker_first_name': 'first',
            'speaker_last_name': 'last',
            'speaker_website': 'http://pywaw.org/',
            'speaker_phone': '123',
            'speaker_email': 'email@pywaw.org',
            'speaker_biography': 'short bio',
            'speaker_photo': files.create_inmemory_image(),
        }
        request = self.factory.post(data=data)

        self.view(request, data=data)

        self.assertEqual(models.Talk.objects.count(), 1)
        saved_talk = models.Talk.objects.all()[0]
        self.assertEqual(saved_talk.title, data['talk_title'])
        self.assertEqual(saved_talk.description, data['talk_description'])
        self.assertEqual(saved_talk.speakers.count(), 1)
        saved_speaker = saved_talk.speakers.all()[0]
        self.assertEqual(saved_speaker.first_name, data['speaker_first_name'])
        self.assertEqual(saved_speaker.last_name, data['speaker_last_name'])
        self.assertEqual(saved_speaker.website, data['speaker_website'])
        self.assertEqual(saved_speaker.phone, data['speaker_phone'])
        self.assertEqual(saved_speaker.email, data['speaker_email'])
        self.assertEqual(saved_speaker.biography, data['speaker_biography'])
        self.assertTrue(saved_speaker.photo)

    @override_settings(TALK_PROPOSAL_RECIPIENTS=['admin1@email.com', 'admin2@email.com'])
    def test_send_email_to_admins(self):
        speaker = SpeakerFactory()
        data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'speaker': speaker.id,
        }
        request = self.factory.post(data=data)

        self.view(request, data=data)

        saved_talk = models.Talk.objects.all()[0]
        context = {
            'talk': saved_talk,
            'site': get_current_site(request),
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

    def test_redirect_to_confirmation_page(self):
        data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'speaker': SpeakerFactory().id,
        }
        request = self.factory.post(data=data)

        response = self.view(request, data=data)

        self.assert_redirect(response, reverse('meetups:talk_proposal_confirmation'))
