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

DISCORD_FORM_WEBHOOK_URL = env.str("DISCORD_FORM_WEBHOOK_URL")

