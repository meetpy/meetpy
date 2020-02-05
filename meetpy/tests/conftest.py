# coding: utf-8

from datetime import date

import pytest

from meetups.models import MeetupType
from tests.factories import MeetupFactory


@pytest.fixture
def techtalk():
    return MeetupType.objects.create(name='Tech Talks', slug='tech-talks')


@pytest.fixture
def openspace():
    return MeetupType.objects.create(name='Open Space', slug='open-space')


@pytest.fixture
def meetup(techtalk):
    def _meetup(number=1, type=techtalk, date=date(2018, 1, 1)):
        return MeetupFactory(
            meetup_type=type,
            number=number,
            date=date,
        )

    return _meetup
