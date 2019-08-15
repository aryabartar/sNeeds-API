from django.db import models
from sNeeds.apps.customAuth.models import CustomUser


def path_for_uploading_file(instance, filename):
    return "tweet/{email}/{filename}".format(email=instance.sender.email, filename=filename)


class TweetModel(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    date_created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False, blank=False, null=False)
    edited = models.BooleanField(default=False)
    file = models.FileField(upload_to=path_for_uploading_file, null=True, blank=True)
    text = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return self.text


# class FileMessageModel(MessageModel):
#     file = models.FileField(upload_to=path_for_uploading_file, null=False, blank=False)
#
#
# class TextMessageModel(MessageModel):
#     text = models.CharField(max_length=256, blank=False, null=False)
