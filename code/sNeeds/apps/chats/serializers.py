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
        fields = ['id', 'chat', 'message', 'updated', 'created']
        extra_kwargs = {
            'sender': {'read_only': True},
        }

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        chat = attrs.get('chat')
        if user != chat.user and user != chat.consultant.user:
            raise ValidationError("User has no access to send message in this chat.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        obj = Message.objects.create(sender=user, **validated_data)
        return obj
