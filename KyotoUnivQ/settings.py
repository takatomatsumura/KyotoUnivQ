"""
Django settings for KyotoUnivQ project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oaab#2kr%trbj2h-w9ycf0&f$7dgi2+p=37!cjw$*y0@26pq77'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'Qapp',
    'Accounts',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'KyotoUnivQ.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'KyotoUnivQ.wsgi.application'


# Database

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    }
}


# Password validation

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


# Interationalization

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Django - allauth

SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
LOGIN_REDIRECT_URL = 'Qpp:index'
ACCOUNT_LOGIN_REDIRECT_URL = 'Qapp:index'
ACCOUNT_LOGOUT_ON_GET = True
DEFAULT_FROM_EMAIL = 'KyotoUnivQ@email.com'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# LOGGING

LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : False,

    'loggers' : {
        'django' : {
            'handlers' : ['console'],
            'level' : 'INFO',
        },
        'Accounts' : {
            'handlers' : ['console'],
            'level' : 'INFO',
        },
        'Qapp' : {
            'handlers' : ['console'],
            'level' : 'INFO',
        }, 
    },

    'handlers' : {
        'console' : {
            'level' : 'DEBUG',
            'class' : 'logging.StreamHandler',
            'formatter' : 'dev'
        },
    },

    'formatters' : {
        'dev' : {
            'format' : '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
                ])
        },
    }
}


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'Qapp/static/'),
    os.path.join(BASE_DIR, 'Accounts/static/'),
    )
STATIC_URL = '/static/'
AUTH_USER_MODEL = 'Accounts.CustomUser'
MEDIA＿ROOT = os.path.join(BASE_DIR, 'img')
MEDIA_URL = '/img/'
LOGIN_REDIRECT_URL = 'friends'
LOGOUT_REDIRECT_URL = 'index'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
