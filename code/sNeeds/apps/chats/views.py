from django.db.models import Q

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat
from . import serializers


class ChatListAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        qs = Chat.objects.filter(Q(user=user) | Q(consultant__user=user))
        return qs
