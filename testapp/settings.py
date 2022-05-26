import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'secret_key')

DEBUG = os.getenv('DJANGO_DEBUG') == 'true'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'formset',
    'testapp',
]

if os.getenv('DATABASE_ENGINE') == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT', 5432),
            'CONN_MAX_AGE': 900,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': Path(__file__).parent / 'test.db',  # live_server requires a file rather than :memory:
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USE_TZ = True

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'testapp.urls'

STATICFILES_DIRS = [
    ('node_modules', BASE_DIR / 'node_modules'),
]

STATIC_ROOT = Path(os.getenv('DJANGO_STATIC_ROOT', BASE_DIR / 'staticfiles'))

STATIC_URL = '/static/'

MEDIA_ROOT = Path(os.getenv('DJANGO_WORKDIR', BASE_DIR / 'workdir')) / 'media'

MEDIA_URL = '/media/'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'tests/templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'wsgi.application'
