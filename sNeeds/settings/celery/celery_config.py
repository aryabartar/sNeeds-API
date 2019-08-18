from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Other Celery settings
CELERY_BEAT_SCHEDULE = {
    'create-room': {
        'task': 'sNeeds.apps.videochats.tasks.create_rooms_from_sold_time_slots',
        'schedule': crontab(minute='*/1'),
    },
}
