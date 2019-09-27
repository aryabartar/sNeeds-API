from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

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


class AbstractMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.sender != self.chat.user and self.sender != self.chat.consultant:
            raise ValidationError("Sender is not user or consultant.")

    class Meta:
        abstract = True


class Message(AbstractMessage):
    message = models.CharField(max_length=2048)


class File(AbstractMessage):
    file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'xls'])]
    )


class Voice(AbstractMessage):
    file = models.FileField()


class Image(AbstractMessage):
    image = models.ImageField()
