import os

from .settings import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "logs.log"),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


DEBUG = False

ALLOWED_HOSTS = [
    '193.176.241.131', '127.0.0.1', 'localhost', '0.0.0.0'
]

CORS_ORIGIN_ALLOW_ALL = DEBUG

STATIC_ROOT = "/static_files/"

