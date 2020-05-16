from enum import Enum

from django.db import models
from enumfields import EnumIntegerField


class NotificationType(Enum):
    sold_time_slot_reminder = 1


class Notification(models.Model):
    send_date = models.DateTimeField()
    sent = models.BooleanField(default=False)

    user_type = EnumIntegerField(enum=NotificationType)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_sold_time_slot_reminder(self):
        return self.user_type == NotificationType.sold_time_slot_reminder

class EmailNotification(Notification):
    email = models.EmailField()

    data_dict = {}

    def get_data_dict(self):
        return str(self.data_dict)
