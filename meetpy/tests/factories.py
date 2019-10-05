from datetime import datetime, timedelta

import factory
from factory.fuzzy import FuzzyNaiveDateTime

from meetups import models


class MeetupFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Meetup

    number = factory.Sequence(lambda n: n)
    date = FuzzyNaiveDateTime(start_dt=datetime.utcnow()-timedelta(days=30*6), end_dt=datetime.utcnow()+timedelta(days=30*6))


class MeetupTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.MeetupType

    name = 'Tech Talk'
    slug = 'tech-talk'
    has_agenda = True


class SpeakerFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Speaker

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    biography = factory.Faker('sentence', nb_words=30)


class TalkFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Talk

    title = factory.Faker('sentence', nb_words=6)
    description = factory.Faker('sentence', nb_words=40)
    order = factory.Sequence(lambda n: n)


class SponsorFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Sponsor

    name = factory.Faker('company')
    description = factory.Faker('sentence', nb_words=40)


class TalkProposalFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.TalkProposal

    message = factory.Faker('sentence')
    date_submitted = FuzzyNaiveDateTime(start_dt=datetime.utcnow()-timedelta(days=30*6), end_dt=datetime.utcnow()+timedelta(days=30*6))
