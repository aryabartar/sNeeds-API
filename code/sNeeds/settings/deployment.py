import os

from .settings import *

DEBUG = False

ALLOWED_HOSTS = [
    '193.176.241.131', '127.0.0.1', 'localhost', '0.0.0.0'
]

CORS_ORIGIN_ALLOW_ALL = DEBUG


STATIC_ROOT = "/static_files/"
