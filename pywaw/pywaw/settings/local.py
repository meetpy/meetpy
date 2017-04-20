from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MEDIA_ROOT = os.path.join(LOCAL_STATIC_ROOT, 'upload')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../sqlite.db',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS += ['localhost']