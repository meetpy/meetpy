import environ

from .base import *

env = environ.Env()

DEBUG = env.bool('DEBUG', default=False)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../../media')

DATABASES = {'default': env.db('DATABASE_URL')}

SECRET_KEY = env.str('SECRET_KEY')

EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

DISCORD_FORM_WEBHOOK_URL = env.str("DISCORD_FORM_WEBHOOK_URL", None)

RECAPTCHA_ENABLED = env.bool("RECAPTCHA_ENABLED", False)

if RECAPTCHA_ENABLED:
    from captcha.constants import TEST_PUBLIC_KEY, TEST_PRIVATE_KEY

    RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_SITE_KEY", TEST_PUBLIC_KEY)
    RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_SECRET_KEY", TEST_PRIVATE_KEY)
    SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

    INSTALLED_APPS += (
        "captcha",
    )
