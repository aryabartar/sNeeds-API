"""
WSGI config for sNeeds project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
DEPLOYMENT = int(os.environ.get('DJANGO_DEPLOYMENT', default=0))

if DEPLOYMENT == 0:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sNeeds.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sNeeds.settings.deployment')

application = get_wsgi_application()
