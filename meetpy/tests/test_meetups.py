# coding=utf-8

from datetime import datetime

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.utils import override_settings
from djet import files, testcases, assertions

from meetups import models, views, forms
from tests.factories import MeetupFactory, SpeakerFactory, TalkFactory


class MeetupManagerTest(TestCase):

    def test_upcoming_if_exists(self):
        MeetupFactory(date=datetime(2000, 1, 1))
        next_meetup = MeetupFactory(date=datetime(2000, 2, 1))

        upcoming_meetup = models.Meetup.objects.get_upcoming(date=datetime(2000, 1, 15))

        self.assertEqual(next_meetup, upcoming_meetup)

    def test_upcoming_if_not_exists(self):
        with self.assertRaises(models.Meetup.DoesNotExist):
            models.Meetup.objects.get_upcoming(date=datetime(2000, 1, 15))


class SlugifyUploadToTest(TestCase):

    def test_filename(self):
        speaker = SpeakerFactory(first_name='Guido', last_name='Van Rossüm')
        upload_to = models.SlugifyUploadTo(settings.SPEAKER_PHOTOS_DIR, ['first_name', 'last_name'])

        path = upload_to(speaker, 'bdfl.png')

        self.assertEqual(path, settings.SPEAKER_PHOTOS_DIR + '/guido-van-rossum.png')


class TalkProposalCreateViewTest(testcases.ViewTestCase, assertions.StatusCodeAssertionsMixin):
    view_class = views.TalkProposalCreateView

    def setUp(self):
        self.speaker = SpeakerFactory()
        meetup = MeetupFactory(date=datetime(2000, 1, 1))
        talk = TalkFactory()
        self.speaker.talks.add(talk)
        meetup.talks.add(talk)
        self.url = reverse('meetups:talk_proposal')

    def test_save_talk_proposal_with_existing_speaker(self):
        data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'talk_language': 'pl',
            'speaker': self.speaker.id,
            'message': 'some comment',
        }
        request = self.factory.post(data=data)

        self.view(request)

        self.assertEqual(models.TalkProposal.objects.count(), 1)
        talk_proposal = models.TalkProposal.objects.get()
        self.assertEqual(talk_proposal.message, data['message'])
        self.assertEqual(models.Talk.objects.count(), 2)
        saved_talk = models.Talk.objects.get(title='some title')
        self.assertEqual(saved_talk.description, data['talk_description'])
        self.assertEqual(saved_talk.speakers.count(), 1)
        self.assertEqual(saved_talk.speakers.all()[0], self.speaker)

    @override_settings(DEFAULT_FILE_STORAGE='djet.files.InMemoryStorage')
    def test_save_talk_proposal_with_new_speaker(self):
        data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'talk_language': 'pl',
            'speaker_first_name': 'first',
            'speaker_last_name': 'last',
            'speaker_website': 'http://pywaw.org/',
            'speaker_phone': '123',
            'speaker_email': 'email@pywaw.org',
            'speaker_biography': 'short bio',
            'speaker_photo': files.create_inmemory_image(),
            'message': 'some comment',
        }
        request = self.factory.post(data=data)

        self.view(request, data=data)

        self.assertEqual(models.TalkProposal.objects.count(), 1)
        talk_proposal = models.TalkProposal.objects.get()
        self.assertEqual(talk_proposal.message, data['message'])
        talk = talk_proposal.talk
        self.assertEqual(talk.title, data['talk_title'])
        self.assertEqual(talk.description, data['talk_description'])
        self.assertEqual(talk.speakers.count(), 1)
        speaker = talk.speakers.get()
        self.assertEqual(speaker.first_name, data['speaker_first_name'])
        self.assertEqual(speaker.last_name, data['speaker_last_name'])
        self.assertEqual(speaker.website, data['speaker_website'])
        self.assertEqual(speaker.phone, data['speaker_phone'])
        self.assertEqual(speaker.email, data['speaker_email'])
        self.assertEqual(speaker.biography, data['speaker_biography'])
        self.assertTrue(speaker.photo)

    @override_settings(TALK_PROPOSAL_RECIPIENTS=['admin1@email.com', 'admin2@email.com'])
    def test_send_email_to_admins(self):
        data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'talk_language': 'pl',
            'speaker': self.speaker.id,
        }
        request = self.factory.post(data=data)

        self.view(request, data=data)

        talk = models.TalkProposal.objects.get()
        context = {
            'talk_proposal': talk,
            'site': get_current_site(request),
            'page_address': settings.CONSTANT['GROUP_PAGE_ADDRESS_SHORT'],
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

    @override_settings(RECAPTCHA_ENABLED=False)
    def test_redirect_to_confirmation_page(self):
        """Test that form submission redirects to the confirmation page."""
        data = {
            'talk_title': 'some title',
            'talk_description': 'some desc',
            'talk_language': 'pl',
            'speaker': self.speaker.id,
            'message': '',
            'without_owner': False,
        }
        
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('meetups:talk_proposal_confirmation'))
        self.assertEqual(models.TalkProposal.objects.count(), 1)


class TalkProposalFormTest(TestCase):

    def test_accepts_when_existing_speaker_is_set_and_new_speaker_fields_are_not(self):
        speaker = SpeakerFactory()
        meetup = MeetupFactory(date=datetime(2000, 1, 1))
        talk = TalkFactory()
        speaker.talks.add(talk)
        meetup.talks.add(talk)
        form = forms.TalkProposalForm(data={
            'talk_title': 'title',
            'talk_description': 'description',
            'talk_language': 'pl',
            'speaker': speaker.id,
            'without_owner': False,
        })

        self.assertTrue(form.is_valid())

    def test_accepts_when_all_required_new_speaker_fields_are_set_and_existing_speaker_is_not(self):
        form = forms.TalkProposalForm(
            data={
                'talk_title': 'title',
                'talk_description': 'description',
                'talk_language': 'pl',
                'speaker_first_name': 'first',
                'speaker_last_name': 'last',
                'speaker_phone': '123',
                'speaker_email': 'email@email.com',
                'speaker_biography': 'short bio',
                'without_owner': False,
            },
            files={
                'speaker_photo': files.create_inmemory_image(),
            },
        )

        self.assertTrue(form.is_valid())

    def test_rejects_when_not_all_required_new_speaker_fields_are_set_and_existing_speaker_is_not(self):
        form = forms.TalkProposalForm(data={
            'talk_title': 'title',
            'talk_description': 'description',
            'talk_language': 'pl',
            'speaker_first_name': 'first',
            'without_owner': False,
        })

        self.assertFalse(form.is_valid())


def test_talk_is_valid_without_speaker():
    form = forms.TalkProposalForm(
        data={
            'talk_title': 'title',
            'talk_description': 'description',
            'talk_language': 'pl',
            'without_owner': True,
        }
    )

    assert form.is_valid()
