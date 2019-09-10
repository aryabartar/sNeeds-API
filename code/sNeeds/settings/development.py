from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['193.176.241.131', '127.0.0.1', 'localhost', '0.0.0.0']
CORS_ORIGIN_ALLOW_ALL = DEBUG

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sneeds',
        'USER': 'sneeds',
        'PASSWORD': 'temp',
        'HOST': '192.168.192.1',
        'PORT': '5432',
    }
}

STATIC_ROOT = "/static_files/"
