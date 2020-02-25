from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic, View

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import ChatOwnerPermission, MessageOwnerPermission

from .models import (Chat, Message, TextMessage, VoiceMessage, FileMessage, ImageMessage)
from .serializers import ChatSerializer, MessagePolymorphicSerializer
from .forms import MessageFilterForm


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
        message_type = self.request.query_params.get("messageType", None)
        message_types = {
            "TextMessage": TextMessage,
            "FileMessage": FileMessage,
            "ImageMessage": ImageMessage,
            "VoiceMessage": VoiceMessage
        }
        if message_type in message_types:
            qs = Message.objects.filter(
                polymorphic_ctype=ContentType.objects.get_for_model(message_types[message_type])
            )
        else:
            qs = Message.objects.all()
        user = self.request.user
        message_qs = qs.filter(sender=user).order_by('-created')
        return message_qs


class MessageDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = MessagePolymorphicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        message_qs = Message.objects.filter(sender=user).order_by('-created')
        return message_qs


class AdminChatListView(UserPassesTestMixin, generic.ListView):
    template_name = "chats/admin_chat_list.html"
    model = Chat

    def test_func(self):
        if not self.request.user.is_anonymous:
            if self.request.user.is_superuser:
                return True
        return False


class AdminChatFormView(generic.detail.SingleObjectMixin, generic.FormView):
    template_name = "chats/admin_chat_detail.html"
    form_class = MessageFilterForm
    object = Message


class AdminChatDetailView(UserPassesTestMixin, generic.DetailView):
    template_name = "chats/admin_chat_detail.html"
    model = Chat
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        chat_id = self.kwargs['id']
        data['chat_messages'] = Message.objects.filter(chat=chat_id)
        data['form'] = MessageFilterForm()
        return data

    def test_func(self):
        if not self.request.user.is_anonymous:
            if self.request.user.is_superuser:
                return True
        return False


class AdminChatView(View):

    def get(self, request, *args, **kwargs):
        view = AdminChatDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AdminChatFormView.as_view()
        return view(request, *args, **kwargs)
