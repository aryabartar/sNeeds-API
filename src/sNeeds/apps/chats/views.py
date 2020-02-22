from django.db.models import Q

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import ChatOwnerPermission, MessageOwnerPermission

from .models import (Chat, Message, TextMessage, VoiceMessage, FileMessage, ImageMessage)
from .serializers import ChatSerializer, MessagePolymorphicSerializer


class ChatListAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        qs = Chat.objects.get_all_user_chats(user)
        return qs


class ChatDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (ChatOwnerPermission, permissions.IsAuthenticated,)


class MessageListAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessagePolymorphicSerializer
    filter_backends = [filters.OrderingFilter,
                       DjangoFilterBackend]
    ordering_fields = ['created']
    filterset_fields = ["chat", "sender"]

    def get_queryset(self):
        user = self.request.user
        message_qs = Message.objects.filter(sender=user).order_by('-created')
        return message_qs


class MessageDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = MessagePolymorphicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        message_qs = Message.objects.filter(sender=user).order_by('-created')
        return message_qs
