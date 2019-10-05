from datetime import datetime, timedelta

import factory
from factory.fuzzy import FuzzyNaiveDateTime

from meetups import models


class MeetupFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Meetup

    number = factory.Sequence(lambda n: n)
    date = FuzzyNaiveDateTime(start_dt=datetime.utcnow()-timedelta(days=30*6), end_dt=datetime.utcnow()+timedelta(days=30*6))



class SpeakerFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Speaker

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class TalkFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Talk

    title = factory.Faker('sentence', nb_words=6)
