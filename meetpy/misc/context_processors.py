import platform
import subprocess

import django
import functools
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def group_info(request):
    return {
        'group': {
            'name': settings.CONSTANT['GROUP_NAME'],
            'logo_path': settings.CONSTANT['LOGO_PATH'],
            'page_address': settings.CONSTANT['GROUP_PAGE_ADDRESS_LONG'],
            'city': settings.CONSTANT['GROUP_CITY'],
            'city_genitive': settings.CONSTANT['GROUP_CITY_GENITIVE'],
            'city_ablative': settings.CONSTANT['GROUP_CITY_ABLATIVE'],
            'city_adjective': settings.CONSTANT['GROUP_CITY_ADJECTIVE'],
            'city_locative': settings.CONSTANT['GROUP_CITY_LOCATIVE'],
            'email': settings.CONSTANT['CONTACT_EMAIL'],
            'social': settings.CONSTANT['SOCIAL_MEDIA'],
            'github': settings.CONSTANT['GITHUB'],
            'presentation_length': settings.CONSTANT['PRESENTATION_LENGTH']
        }
    }


def system_info(request):
    return {
        'system': {
            'django': django.get_version(),
            'python': platform.python_version(),
            'website': get_website_version(),
        }
    }


def current_site(request):
    return {
        'site': get_current_site(request),
    }


@functools.lru_cache(maxsize=1)
def get_website_version():
    command = 'git rev-parse HEAD'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, cwd=settings.PROJECT_ROOT)
    return process.communicate()[0].decode('utf-8')
