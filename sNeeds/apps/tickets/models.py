from django.db import models

from sNeeds.apps.customAuth.models import CustomUser
from sNeeds.apps.account.models import ConsultantProfile


def path_for_uploading_file(instance, filename):
    return "media/tickets/{title}/{filename}".format(title=instance.ticket.title, filename=filename)


class Ticket(models.Model):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.CharField(max_length=256, blank=False, null=False)
    file = models.FileField(upload_to=path_for_uploading_file, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
