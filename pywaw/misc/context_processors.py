import django
import platform


def system_info(request):
    return {
        'system': {
            'django': django.get_version(),
            'python': platform.python_version(),
        }
    }
