from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic, View
from django.shortcuts import render

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import ChatOwnerPermission, MessageOwnerPermission

from .models import (Chat, Message, TextMessage, VoiceMessage, FileMessage, ImageMessage, MESSAGE_TYPES)
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
    permission_classes = (permissions.IsAuthenticated,)
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
    success_url = "/chat/admin/"


class AdminChatDetailView(generic.DetailView):
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


class AdminChatView(UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        view = AdminChatDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AdminChatFormView.as_view()
        return view(request, *args, **kwargs)

    def test_func(self):
        if not self.request.user.is_anonymous:
            if self.request.user.is_superuser:
                return True
        return False


def is_valid_queryparam(param):
    return param != '' and param is not None and param != []


def filter_chats(request):
    qs = Chat.objects.all()
    chat_id = request.GET.get('chat_id')
    user_email = request.GET.get('user_email')
    consultant_email = request.GET.get('consultant_email')

    if is_valid_queryparam(chat_id):
        qs = qs.filter(id=chat_id)
    if is_valid_queryparam(user_email):
        qs = qs.filter(user__email__icontains=user_email)
    if is_valid_queryparam(consultant_email):
        qs = qs.filter(consultant__user__email__icontains=consultant_email)

    return qs


def admin_chat_peek(request):
    qs = filter_chats(request)
    context = {
        'queryset': qs,
    }
    return render(request, "chats/admin_chat_list.html", context)


def filter_messages(request, id):
    qs = Message.objects.filter(chat_id=id)
    text_message_search_character_query = request.GET.get('text_message_search_character')
    send_date_min = request.GET.get('send_date_min')
    send_date_max = request.GET.get('send_date_max')
    sender = request.GET.get('sender')
    selected_message_types = request.GET.getlist('message_type_selector')

    if is_valid_queryparam(text_message_search_character_query):
        qs = qs.filter(textmessage__text_message__icontains=text_message_search_character_query)
    if is_valid_queryparam(send_date_min):
        qs = qs.filter(created__gte=send_date_min)
    if is_valid_queryparam(send_date_max):
        qs = qs.filter(created__lt=send_date_max)
    if is_valid_queryparam(sender) and sender != 'Choose...':  # TODO: If possible make better
        qs = qs.filter(sender__email=sender)
    if is_valid_queryparam(selected_message_types):
        # Converting each type in message_type_selector to its model in django
        model_of_selected_types = []
        for message_type in selected_message_types:
            model_of_selected_types.append(MESSAGE_TYPES[message_type])

        # Converting each model to its associated ContentType
        content_type_for_selected_types = []
        for model in model_of_selected_types:
            content_type_for_selected_types.append(ContentType.objects.get_for_model(model))

        qs = qs.filter(polymorphic_ctype__in=content_type_for_selected_types)

    return qs


# TODO: raise a proper error on not exist
def get_chat_user(id):
    chat_users = []
    try:
        chat = Chat.objects.get(id=id)
    except Chat.DoesNotExist:
        chat = None

    if chat:
        chat_users.append(chat.consultant)
        chat_users.append(chat.user)
    return chat_users


def admin_chat_messages_peek(request, id):
    qs = filter(request, id)
    chat_users = get_chat_user(id)
    context = {
        'queryset': qs,
        'chat_users': chat_users,
        'message_types': MESSAGE_TYPES.keys()
    }
    return render(request, "chats/admin_chat_detail.html", context)
