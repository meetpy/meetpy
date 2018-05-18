from .base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../../media')

with open(os.path.join('./pygroups/settings/pygroups_secret_variables', 'stage.json'), "r") as f:
    secrets.update(json.loads(f.read()))

ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS', secrets)

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
