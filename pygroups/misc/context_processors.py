import functools
import subprocess
import django
import platform
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def group_info(request):
    return {
        'group': {
            'name': settings.GROUP_NAME,
            'logo_path': settings.LOGO_PATH,
            'page_address': settings.GROUP_PAGE_ADDRESS_LONG,
            'city': settings.GROUP_CITY,
            'city_genitive': settings.GROUP_CITY_GENITIVE,
            'city_ablative': settings.GROUP_CITY_ABLATIVE,
            'city_adjective': settings.GROUP_CITY_ADJECTIVE,
            'email': settings.CONTACT_EMAIL,
            'social': settings.SOCIAL_MEDIA,
            'github': settings.GITHUB,
            'presentation_length': settings.PRESENTATION_LENGTH
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
    return process.communicate()[0]
