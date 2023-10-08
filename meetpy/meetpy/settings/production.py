from .base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../../media')


with open(os.path.join('./meetpy/settings/meetpy_secret_variables', 'prod.json')) as f:
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

EMAIL_HOST = get_secret('EMAIL_HOST', secrets)
EMAIL_PORT = int(get_secret('EMAIL_PORT', secrets))
EMAIL_USE_TLS = get_secret('EMAIL_USE_TLS', secrets) == 'true'
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER', secrets)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD', secrets)
SERVER_EMAIL = EMAIL_HOST_USER

RECAPTCHA_ENABLED = CONSTANT.get("RECAPTCHA_ENABLED", False)

if RECAPTCHA_ENABLED:
    RECAPTCHA_PUBLIC_KEY = get_secret("RECAPTCHA_SITE_KEY", secrets)
    RECAPTCHA_PRIVATE_KEY = get_secret("RECAPTCHA_SECRET_KEY", secrets)

    INSTALLED_APPS += (
        "captcha",
    )
