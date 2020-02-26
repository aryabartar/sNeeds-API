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
    return param != '' and param is not None


def filter(request, id):
    qs = Message.objects.filter(chat_id=id)
    text_message_search_character_query = request.GET.get('text_message_search_character')
    send_date = request.GET.get('send_date')
    # title_or_author_query = request.GET.get('title_or_author')
    # view_count_min = request.GET.get('view_count_min')
    # view_count_max = request.GET.get('view_count_max')
    # date_min = request.GET.get('date_min')
    # date_max = request.GET.get('date_max')
    # category = request.GET.get('category')
    # reviewed = request.GET.get('reviewed')
    # not_reviewed = request.GET.get('notReviewed')

    if is_valid_queryparam(text_message_search_character_query):
        qs = qs.filter(textmessage__text_message__icontains=text_message_search_character_query)
    if is_valid_queryparam(send_date):
        qs = qs.filter(created__gte=send_date)
    #
    # elif is_valid_queryparam(id_exact_query):
    #     qs = qs.filter(id=id_exact_query)
    #
    # elif is_valid_queryparam(title_or_author_query):
    #     qs = qs.filter(Q(title__icontains=title_or_author_query)
    #                    | Q(author__name__icontains=title_or_author_query)
    #                    ).distinct()
    #
    # if is_valid_queryparam(view_count_min):
    #     qs = qs.filter(views__gte=view_count_min)
    #
    # if is_valid_queryparam(view_count_max):
    #     qs = qs.filter(views__lt=view_count_max)
    #
    # if is_valid_queryparam(date_min):
    #     qs = qs.filter(publish_date__gte=date_min)
    #
    # if is_valid_queryparam(date_max):
    #     qs = qs.filter(publish_date__lt=date_max)
    #
    # if is_valid_queryparam(category) and category != 'Choose...':
    #     qs = qs.filter(categories__name=category)

    # if reviewed == 'on':
    #     qs = qs.filter(reviewed=True)
    #
    # elif not_reviewed == 'on':
    #     qs = qs.filter(reviewed=False)

    return qs


def admin_chat_peek(request, id):
    qs = filter(request, id)
    context = {
        'queryset': qs,
    }
    return render(request, "chats/admin_chat_detail.html", context)

