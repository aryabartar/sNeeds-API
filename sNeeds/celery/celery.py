import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sNeeds.settings.development')

app = Celery('sneeds')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
