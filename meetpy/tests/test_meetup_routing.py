# coding: utf-8

from datetime import date

import pytest

from tests.tools import redirects, contains, template_used


@pytest.mark.django_db
def test_meetup_specific_routing(client, meetup, techtalk, openspace):
    """
    https://github.com/pykonik/pykonik.org/issues/6
    """

    unique_number = 42
    shared_number = 1

    tt_unique = meetup(unique_number, techtalk)

    tt_shared = meetup(shared_number, techtalk)
    os_shared = meetup(shared_number, openspace)

    response = client.get(f'/{unique_number}/')
    assert redirects(response, tt_unique.get_absolute_url())

    response = client.get(f'/{unique_number}/', follow=True)
    assert template_used(response, 'meetups/meetup_detail.html')
    assert contains(response, tt_unique.description)

    response = client.get(f'/{shared_number}/')
    assert template_used(response, 'meetups/meetup_list.html')
    assert contains(response, tt_shared.get_absolute_url())
    assert contains(response, os_shared.get_absolute_url())


@pytest.mark.django_db
def test_meetup_date_redirect(client, meetup):
    """
    Legacy date-based behaviour
    """
    tt = meetup(date=date(2018, 8, 17))

    response = client.get('/17-08-2018/')
    assert tt.get_absolute_url() == '/tech-talks/1/'
    assert redirects(response, tt.get_absolute_url())

    response = client.get('/17-08-2018/', follow=True)
    assert response.status_code == 200
    assert template_used(response, "meetups/meetup_detail.html")

    response = client.get('/18-08-2019/')
    assert response.status_code == 404
