import functools
import subprocess
import django
import platform
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


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
