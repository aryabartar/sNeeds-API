def chat_last_message_updated(chat):
    from sNeeds.apps.chats.models import Message
    if Message.objects.filter(chat=chat).count() == 0:
        return chat.updated
    return Message.objects.filter(chat=chat).order_by('-updated').first().updated
