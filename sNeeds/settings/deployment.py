from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['193.176.241.131', '127.0.0.1',]
CORS_ORIGIN_ALLOW_ALL = DEBUG

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sneeds',
        'USER': 'sneeds',
        'PASSWORD': '2p@d2!fu-0*&kz01z6zljnwcn)rdbm50n&_5%q)vc*kv_)5ima',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
