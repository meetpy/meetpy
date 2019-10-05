# coding=utf-8
import environ

env = environ.Env()

GROUP_NAME = env('GROUP_NAME', default='GROUP_NAME')  # uppercase
GROUP_PAGE_ADDRESS_SHORT = env('GROUP_PAGE_ADDRESS_SHORT', default='GROUP_PAGE_ADDRESS_SHORT')
GROUP_PAGE_ADDRESS_LONG = env('GROUP_PAGE_ADDRESS_LONG', default='GROUP_PAGE_ADDRESS_LONG')
GROUP_CITY = env('GROUP_CITY', default='GROUP_CITY')
GROUP_CITY_GENITIVE = env('GROUP_CITY_GENITIVE', default='GROUP_CITY_GENITIVE') # examples: Krakowa, Warszawy
GROUP_CITY_ABLATIVE = env('GROUP_CITY_ABLATIVE', default='GROUP_CITY_ABLATIVE')  # examples: Krakowie, Warszawie
GROUP_CITY_ADJECTIVE = env('GROUP_CITY_ADJECTIVE', default='GROUP_CITY_ADJECTIVE')  # examples: Krakowska, Warszawska
GROUP_CITY_LOCATIVE = env('GROUP_CITY_LOCATIVE ', default='GROUP_CITY_LOCATIVE') # examples: krakowskiej, warszawskiej
CONTACT_EMAIL = env('CONTACT_EMAIL', default='CONTACT_EMAIL')
LOGO_PATH = 'group/group_logo.png'
GITHUB = 'https://github.com/meetpy/meetpy'

# Social - leave empty if you don't have specific one
SOCIAL_MEDIA = {
    'meetup': 'http://www.meetup.com/Pykonik/',
    'facebook': 'https://www.facebook.com/Pykonik-87835845639/',
    'twitter': 'http://twitter.com/pykonik',
    'youtube': 'http://youtube.com/pykonik',
}

FEED_TITLE = env('FEED_TITLE', default='FEED_TITLE')
EITHER_EXISTING_OR_NEW_SPEAKER_ERROR = 'Wybierz prelegenta z listy lub wprowadź dane dla nowego.'
PRESENTATION_LENGTH = 25
