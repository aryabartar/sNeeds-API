from django.db.models import Q

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import ChatOwnerPermission, MessageOwnerPermission

from .models import Chat, TextMessage
from . import serializers


class ChatListAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        qs = Chat.objects.get_all_user_chats(user)
        return qs


class ChatDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer
    permission_classes = (ChatOwnerPermission, permissions.IsAuthenticated,)


class TextMessageListAPIView(generics.ListCreateAPIView):
    lookup_field = 'id'
    serializer_class = serializers.TextMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        chats_qs = Chat.objects.get_all_user_chats(user)
        messages_qs = TextMessage.objects.get_chats_messages(chats_qs)
        return messages_qs


class TextMessageDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = TextMessage.objects.all()
    serializer_class = serializers.TextMessageSerializer
    permission_classes = (MessageOwnerPermission, permissions.IsAuthenticated,)
