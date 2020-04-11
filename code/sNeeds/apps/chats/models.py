from django.db.models import Q
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager

from sNeeds.apps.chats.utils import chat_last_message_updated
from sNeeds.apps.consultants.models import ConsultantProfile

User = get_user_model()


def get_file_upload_path(instance, filename):
    return "chats/files/{}/{}/{}".format(instance.chat, timezone.datetime.now(), filename)


def get_image_upload_path(instance, filename):
    return "chats/images/{}/{}/{}".format(instance.chat, timezone.datetime.now(), filename)


def get_voice_upload_path(instance, filename):
    return "chats/voices/{}/{}/{}".format(instance.chat, timezone.datetime.now(), filename)


class ChatManager(models.QuerySet):
    def get_all_user_chats(self, user):
        qs = self._chain().filter(Q(user=user) | Q(consultant__user=user))
        return qs

    def sort_based_on_last_message(self):
        qs = self._chain()
        ordered = sorted(qs, key=chat_last_message_updated, reverse=True)
        return ordered


class MessageManager(PolymorphicManager):
    def get_chats_messages(self, chats_qs):
        queryset = self.get_queryset()

        qs = None
        for chat in chats_qs:

            if qs is None:
                qs = queryset.filter(chat=chat)
            else:
                qs = qs | queryset.filter(chat=chat)

        return qs


class Chat(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    consultant = models.ForeignKey(ConsultantProfile, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ChatManager.as_manager()

    class Meta:
        unique_together = ['user', 'consultant']


class Message(PolymorphicModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
    tag = models.IntegerField(editable=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def clean(self):
        if self.sender != self.chat.user and self.sender != self.chat.consultant.user:
            raise ValidationError("User {} cannot send message to this chat.".format(self.sender))

    def save(self, *args, **kwargs):
        self.tag = Message.objects.filter(chat=self.chat).count() + 1
        super(Message, self).save(*args, **kwargs)


class TextMessage(Message):
    text_message = models.CharField(max_length=2048)


class FileMessage(Message):
    file_field = models.FileField(
        upload_to=get_file_upload_path,
    )


class VoiceMessage(Message):
    voice_field = models.FileField(
        upload_to=get_voice_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'm4a'])]  # TODO: may be changed
    )


class ImageMessage(Message):
    image_field = models.ImageField(
        upload_to=get_image_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )


MESSAGE_TYPES = {
    TextMessage.__name__: TextMessage,
    FileMessage.__name__: FileMessage,
    VoiceMessage.__name__: VoiceMessage,
    ImageMessage.__name__: ImageMessage
}
