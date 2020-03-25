from datetime import timedelta

from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Other Celery settings
CELERY_BEAT_SCHEDULE = {
    'create-room': {
        'task': 'sNeeds.apps.videochats.tasks.create_rooms_from_sold_time_slots',
        'schedule': timedelta(minutes=1),
    },
    'delete-room': {
        'task': 'sNeeds.apps.videochats.tasks.delete_used_rooms',
        'schedule': timedelta(minutes=1),
    },
    'delete-time-slots': {
        'task': 'sNeeds.apps.store.tasks.delete_time_slots',
        'schedule': timedelta(minutes=1),
    },
    'database-regular-backup': {
        'task': 'sNeeds.apps.customUtils.tasks.backup_database',
        'schedule': timedelta(seconds=30),
    },
    'media-regular-backup': {
        'task': 'sNeeds.apps.customUtils.tasks.backup_database',
        'schedule': timedelta(seconds=30),
    },
    'sold-time-slot-start-reminder': {
        'task': 'sNeeds.apps.store.tasks.sold_time_slot_start_reminder',
        'schedule': crontab(hour=18, minute=30),  # In UTC | 10 PM in Iran
    },
}
