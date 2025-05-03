from .base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../../media')

with open(os.path.join('./meetpy/settings/meetpy_secret_variables', 'stage.json'), "r") as f:
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

DISCORD_FORM_WEBHOOK_URL = get_secret("DISCORD_FORM_WEBHOOK_URL", secrets, None)

RECAPTCHA_ENABLED = CONSTANT.get("RECAPTCHA_ENABLED", False)

if RECAPTCHA_ENABLED:
    RECAPTCHA_PUBLIC_KEY = get_secret("RECAPTCHA_SITE_KEY", secrets)
    RECAPTCHA_PRIVATE_KEY = get_secret("RECAPTCHA_SECRET_KEY", secrets)

    INSTALLED_APPS += (
        "django_recaptcha",
    )
