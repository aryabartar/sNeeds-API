from django.db import models


class Notification(models.Model):
    message = models.TextField()

    send_date = models.DateTimeField()
    sent = models.BooleanField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class EmailNotification(Notification):
    email = models.EmailField()
