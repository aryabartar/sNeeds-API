from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from sNeeds.apps.account.models import ConsultantProfile

User = get_user_model()

FILE_TYPES = (
    ('file', 'File'),
    ('picture', 'Picture'),
    ('voice', 'Voice'),
)


class Chat(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    consultant = models.ForeignKey(ConsultantProfile, null=True, on_delete=models.SET_NULL)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
    message = models.CharField(max_length=2048)
    created = models.DateTimeField(auto_now_add=True)


class AbstractFile(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')


class File(AbstractFile):
    file = models.FileField()


class Voice(AbstractFile):
    file = models.FileField()


class Image(AbstractFile):
    image = models.ImageField()
