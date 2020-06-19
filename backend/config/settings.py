"""
Django settings for reactify project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

import json
from six.moves.urllib import request


gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ksy0*&5)&=lxwj-7g+$zepz3#2*vt#os^nbi5o&2#k_s5s6ee@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SITE_ID = 1

"""============================
EMAIL HANDLING
============================"""
ADMINS = (
    ('ABC Company | Sample Office', 'sample.office@gmail.com'),
)

MANAGERS = ADMINS


# When you are playing around with the app and you expect that an email should
# have been sent, just run `./manage.py send_mail` and you will get the mail
# to the ADMINS account, no matter who the real recipient was.
MAILER_EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'

# SMTP definition for MIS [generic email]
GENERIC_EMAIL_HOST_SAMPLE_OFFICE = 'smtp.gmail.com'
GENERIC_EMAIL_PORT_SAMPLE_OFFICE = 587
GENERIC_EMAIL_TLS_SAMPLE_OFFICE = True
GENERIC_FROM_EMAIL_SAMPLE_OFFICE = ADMINS[0][1]
GENERIC_EMAIL_SUBJECT_PREFIX_SAMPLE_OFFICE = ADMINS[0][0]
GENERIC_EMAIL_HOST_USER_SAMPLE_OFFICE = GENERIC_FROM_EMAIL_SAMPLE_OFFICE
GENERIC_EMAIL_HOST_PASSWORD_SAMPLE_OFFICE = "your_gmail_password"

SILENCED_SYSTEM_CHECKS = ['urls.W001']


# Application definition

INSTALLED_APPS = [
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'corsheaders',
    'rest_framework',

    'rest_framework.authtoken',
    'knox',

    'account_app',

    'treebeard',

    # HTML Richtext Editor
    'django_summernote',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Defining location of static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(DATA_DIR, 'static-cdn-local')
MEDIA_ROOT = os.path.join(DATA_DIR, 'media-cdn-local')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

# Defining templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = "config.routing.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

"""
----------------------------------------------
PRODUCTION DB CONNECTION CONFIGURATION [MAIN]
----------------------------------------------
1. This is the main connection configuration
2. This is used for production
"""
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  },
  # 'default': {
  #   'ENGINE': 'django.db.backends.postgresql',
  #   'HOST': '192.168.10.100',
  #   'NAME': 'your-postgresql-db-name',
  #   'PASSWORD': 'your_db_password',
  #   'PORT': '5432',
  #   'USER': 'postgres',
  #   'OPTIONS': {
  #       'options': '-c search_path=public'
  #   },
  # },
  # 'connection2': {
  #   'ENGINE': 'django.db.backends.postgresql',
  #   'HOST': '192.168.10.105',
  #   'NAME': 'your-other-postgresql-db-name',
  #   'PASSWORD': 'your_db_password',
  #   'PORT': '5432',
  #   'USER': 'postgres',
  #   'OPTIONS': {
  #       'options': '-c search_path=public'
  #   },
  # },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_URLS_REGEX = r'^/api.*'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
    'DATETIME_FORMAT': "iso-8601",
}

AUTHENTICATION_BACKENDS = (
    'account_app.utils.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LANGUAGES = (
    ## Customize this
    ('en', 'en'),
)

X_FRAME_OPTIONS = 'SAMEORIGIN'