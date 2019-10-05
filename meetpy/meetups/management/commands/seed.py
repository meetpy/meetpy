from django.core.management.base import BaseCommand, CommandError

from tests.factories import MeetupFactory, TalkFactory, SpeakerFactory


class Command(BaseCommand):
    help = 'Seed development data'

    def handle(self, *args, **options):

        for i in range(10):
            meetup = MeetupFactory.create()
            talk = TalkFactory.create(meetup=meetup)
            talk.speakers.add(SpeakerFactory.create())
            talk = TalkFactory.create(meetup=meetup)
            talk.speakers.add(SpeakerFactory.create())


