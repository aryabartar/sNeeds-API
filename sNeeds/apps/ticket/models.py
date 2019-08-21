from django.db import models

from sNeeds.apps.customAuth.models import CustomUser
from sNeeds.apps.account.models import ConsultantProfile


def path_for_uploading_file(instance, filename):
    return "files/media/ticket/{email}/{filename}".format(email=instance.ticket.title, filename=filename)


class Ticket(models.Model):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        title_splited = self.title.split(' ')
        title = ' '.join(title_splited[:5])
        title += "..."
        return title


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.CharField(max_length=256, blank=False, null=False)
    file = models.FileField(upload_to=path_for_uploading_file, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        text_splited = self.text.split(' ')
        text = ' '.join(text_splited[:5])
        text += "..."
        return text