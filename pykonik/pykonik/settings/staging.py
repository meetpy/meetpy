from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../../media')

with open(os.path.join('./pykonik/settings/pykonik_secret_variables', 'stage.json'), "r") as f:
    secrets.update(json.loads(f.read()))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME', secrets),
        'USER': get_secret('DB_USER', secrets),
        'PASSWORD': get_secret('DB_PASSWORD', secrets),
        'HOST': get_secret('DB_HOST', secrets),
        'PORT': get_secret('DB_PORT', secrets),
    }
}