from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="chat:chat-detail", lookup_field='id')
    other_name = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id', 'url', 'other_name'
        ]

    def get_other_name(self, obj):
        request = self.context.get('request')
        user = request.user

        if user == obj.user:
            return obj.consultant.user.get_full_name()

        return obj.user.get_full_name()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
