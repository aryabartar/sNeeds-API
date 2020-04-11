from django.utils import timezone


def chat_last_message_updated(chat):
    from sNeeds.apps.chats.models import Message

    if Message.objects.filter(chat=chat).count() == 0:
        return timezone.make_aware(timezone.datetime(10, 1, 1, *[0] * 4), timezone.get_default_timezone())
    return Message.objects.filter(chat=chat).order_by('-updated').first().updated
