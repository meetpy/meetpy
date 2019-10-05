import os

import dj_database_url
import environ
from dotenv import load_dotenv

load_dotenv()

env = environ.Env()

DEBUG = env.bool('DEBUG', default=False)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# Group constants

GROUP_NAME = env.str('GROUP_NAME')  # uppercase
GROUP_PAGE_ADDRESS_SHORT = env.str('GROUP_PAGE_ADDRESS_SHORT')
GROUP_PAGE_ADDRESS_LONG = env.str('GROUP_PAGE_ADDRESS_LONG')
GROUP_CITY = env.str('GROUP_CITY')
GROUP_CITY_GENITIVE = env.str('GROUP_CITY_GENITIVE')
GROUP_CITY_ABLATIVE = env.str('GROUP_CITY_ABLATIVE')
GROUP_CITY_ADJECTIVE = env.str('GROUP_CITY_ADJECTIVE')
GROUP_CITY_LOCATIVE = env.str('GROUP_CITY_LOCATIVE')
CONTACT_EMAIL = env.str('CONTACT_EMAIL')
LOGO_PATH = env.str('LOGO_PATH')
GITHUB = env.str('GITHUB')

# Social - leave empty if you don't have specific one
SOCIAL_MEDIA = {
    'meetup': env.str('SOCIAL_MEDIA_MEETUP'),
    'facebook': env.str('SOCIAL_MEDIA_FACEBOOK'),
    'twitter': env.str('SOCIAL_MEDIA_TWITTER'),
    'youtube': env.str('SOCIAL_MEDIA_YOUTUBE'),
}

FEED_TITLE = env.str('FEED_TITLE')
EITHER_EXISTING_OR_NEW_SPEAKER_ERROR = env.str('EITHER_EXISTING_OR_NEW_SPEAKER_ERROR')
PRESENTATION_LENGTH = env.int('PRESENTATION_LENGTH')

# Django settings

ADMINS = (
    ('Admin', env.str('ADMIN_EMAIL', '')),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': env.str('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': env.str('DB_NAME', '../sqlite.db'),
        'USER': env.str('DB_USER', ''),
        'PASSWORD': env.str('DB_PASSWORD', ''),
        'HOST': env.str('DB_HOST', ''),
        'PORT': env.str('DB_PORT', ''),
    }
}

DB_URL = env.str("DB_URL", '')

if DB_URL:
    DATABASES['default'] = dj_database_url.parse(DB_URL, conn_max_age=600)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = ['.pywaw.org', '178.62.28.109']
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, '../../static')
LOCAL_STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
STORAGE_BACKEND = env.str('MEDIA_STORAGE_BACKEND', 'local')

if STORAGE_BACKEND == 's3':
    # TODO: setup s3
    pass
else:  # local or simply default
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, env.str('MEDIA_RELATIVE_PATH'))

SPONSOR_LOGOS_DIR = 'sponsors'
MEETUP_PHOTOS_DIR = 'meetup_photos'
SPEAKER_PHOTOS_DIR = 'speakers'
SLIDES_FILES_DIR = 'slides'
PARTNER_LOGOS_DIR = 'partners'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    LOCAL_STATIC_ROOT,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = env.str('SECRET_KEY')

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'meetpy.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'meetpy.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'meetups',
    'misc',
    'embed_video',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    TALK_PROPOSAL_RECIPIENTS = [CONTACT_EMAIL]
except NameError:
    TALK_PROPOSAL_RECIPIENTS = []
    print('WARNING - Your meetup-specific data might not be set.'
          'Please prepare the group_constants/constants.py file '
          'and make sure that CONCACT_EMAIL variable is set')


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'misc.context_processors.group_info',
                'misc.context_processors.system_info',
                'misc.context_processors.current_site',
                'meetups.context_processors.stats'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
                # 'django.template.loaders.eggs.Loader',
            ],
            'debug': DEBUG
        },
    }
]

EMAIL_BACKEND = env.str('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT', 25)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = EMAIL_HOST_USER

