from django.core.management.base import BaseCommand, CommandError

from tests.factories import MeetupFactory, TalkFactory, SpeakerFactory, MeetupTypeFactory, SponsorFactory


class Command(BaseCommand):
    help = 'Seed development data'

    def handle(self, *args, **options):
        meetup_type = MeetupTypeFactory.create()

        for i in range(10):
            meetup = MeetupFactory.create(meetup_type=meetup_type)
            talk = TalkFactory.create(meetup=meetup)
            talk.speakers.add(SpeakerFactory.create())
            talk = TalkFactory.create(meetup=meetup)
            talk.speakers.add(SpeakerFactory.create())
            meetup.sponsors.add(SponsorFactory())
            meetup.sponsors.add(SponsorFactory())


