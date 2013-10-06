import django
import platform
from django.contrib.sites.models import get_current_site


def system_info(request):
    return {
        'system': {
            'django': django.get_version(),
            'python': platform.python_version(),
        }
    }


def current_site(request):
    return {
        'site': get_current_site(request),
    }
