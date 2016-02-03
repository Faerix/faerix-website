#encoding: utf8
"""
Django settings for faerix project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DJANGO_DEBUG", ""))

if DEBUG:
    print("Warning:  debug mode !", file=sys.stderr)

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'conv.User'

LOGIN_REDIRECT_URL = 'news'
# Application definition

INSTALLED_APPS = (
    'conv',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',
    'front',
    'braces',
    'hijack',
    'compat', # for hijack
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'faerix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'conv.context_processors.inject_sponsors',
                'conv.context_processors.inject_news_count',
                'conv.context_processors.inject_static_url',

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'faerix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(BASE_DIR, "my.cnf"),
            },
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'FR-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/assets/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "assets/static/")

MEDIA_ROOT = os.path.join(BASE_DIR, "assets/media/")

MEDIA_URL = '/assets/media/'

HIJACK_LOGIN_REDIRECT_URL = '/'  # Where admins are redirected to after hijacking a user
HIJACK_LOGOUT_REDIRECT_URL = '/admin/conv/user/'  # Where admins are redirected to after releasing a user
HIJACK_DISPLAY_ADMIN_BUTTON = False
HIJACK_USE_BOOTSTRAP = True
HIJACK_AUTHORIZE_STAFF = True
HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF = True

#################################################

MAX_N_PLAYERS = 99
DEFAULT_FROM_EMAIL = "conv@faerix.net"
SERVER_EMAIL = "webmaster@faerix.net" # redirige sur info@faerix.polytechnique.org
ADMINS = [("Webmaster Faërix", "webmaster@faerix.net")]
