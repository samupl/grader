from lib.default_config_parser import DefaultConfigParser

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Config file reader
config = DefaultConfigParser()
config.read(os.path.join(BASE_DIR, 'grader.conf'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(!)&6yb5o*lh*ddgp@7$m#k8)c3(4!qm#=5eus)wm8-)k%(sfs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('debug', 'debug', default=False)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party applications
    'debug_toolbar',
    'bootstrap3',
    'django_markdown2',
    'django_summernote',
    # Local project applications
    'apps.breadcrumbs',
    'apps.grader_core',
    'apps.grader_checker',
    'apps.grader_environments',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'grader.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG
        },
    },
]

WSGI_APPLICATION = 'grader.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGES = [
    ('en', 'English'),
    ('pl', 'Polski'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'media')]  # For debug purposes only


def show_toolbar(_):
    return DEBUG


INTERNAL_IPS = ['127.0.0.1', '79.186.212.146']
SHOW_TOOLBAR_CALLBACK = show_toolbar


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s  %(process)d %(threadName)s]  %(name)s  %(levelname)s:  %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'grader': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },

        'paramiko': {
            'handlers': ['console'],
            'level': 'ERROR',
        }
    },
}


LOGIN_REDIRECT_URL = 'frontend:home'
