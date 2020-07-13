import json
from enum import Enum
from jsonfield import JSONField

from django.db import models
from enumfields import EnumIntegerField


class NotificationType(Enum):
    sold_time_slot_reminder = 1


class NotificationManager(models.Manager):
    def create_sold_time_slot_reminder(self, **kwargs):
        obj = self.create(type=NotificationType.sold_time_slot_reminder, **kwargs)
        return obj


class Notification(models.Model):
    send_date = models.DateTimeField()
    sent = models.BooleanField(default=False)

    type = EnumIntegerField(enum=NotificationType)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_sold_time_slot_reminder(self):
        return self.type == NotificationType.sold_time_slot_reminder


class EmailNotification(Notification):
    email = models.EmailField()
    data_json = JSONField()

    objects = NotificationManager()

    def get_data_dict(self):
        return json.loads(self.data_json)


class SoldTimeSlotEmailNotification(EmailNotification):
    sold_time_slot_id = models.PositiveIntegerField()
