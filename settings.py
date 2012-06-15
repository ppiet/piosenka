import os

# Django settings both for production and developement environment

DEVELOPEMENT_SERVER_USERNAMES = ["dx",] # append your local username if You wish / need to

PRODUCTION_SETTINGS = not (os.getenv("USER") in DEVELOPEMENT_SERVER_USERNAMES)


DEBUG = not PRODUCTION_SETTINGS
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Przemyslaw Pietrzkiewicz', 'pietrzkiewicz@gmail.com'),
)

MANAGERS = ADMINS

try:
    from settings_production import DATABASES
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'playground',
            'USER': 'playboy',
            'PASSWORD': 'play',
            'HOST': '',
            'PORT': '',
        }
    }

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = False
USE_L10N = True

import os
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

MEDIA_ROOT = os.path.join(PROJECT_PATH, "site_media", "upload")

MEDIA_URL = "/site_media/upload/"

STATIC_ROOT = os.path.join(PROJECT_PATH, "site_media", "native")

STATIC_URL = '/site_media/native/'

STATICFILES_DIRS = (
    ("", os.path.join(PROJECT_PATH, "static")),
    ("scripts", os.path.join(PROJECT_PATH, "songs", "scripts")),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o@c*tih1vzy69-#wv16(^a7sgsv5l^vw7fah&+ttvyjyi@7)jr'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'urls'

FILE_CHARSET = "utf-8-sig"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'songs.views.songs_context'
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_PATH, "index")

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'blog',
    'artists',
    'songs',
    'events',
    'dxlibrary',
    'haystack',
    'south',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

INTERNAL_IPS = ('127.0.0.1',)
