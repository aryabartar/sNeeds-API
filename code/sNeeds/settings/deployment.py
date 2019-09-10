from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CORS_ORIGIN_ALLOW_ALL = DEBUG

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sneeds',
        'USER': 'sneeds',
        'PASSWORD': 'temp',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STATIC_ROOT = "/static_files/"
