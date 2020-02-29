from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_polymorphic.serializers import PolymorphicSerializer

from sNeeds.apps.store.models import SoldTimeSlotSale
from .models import Chat, Message, TextMessage, VoiceMessage, FileMessage, ImageMessage


class ChatSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="chat:chat-detail", lookup_field='id')
    other_person = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id',
            'url',
            'other_person'
        ]

    def get_other_person(self, obj):
        from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer

        request = self.context.get('request')
        user = request.user

        if user == obj.user:
            other_person = obj.consultant.user
        else:
            other_person = obj.user

        return SafeUserDataSerializer(other_person).data


class MessageSerializer(serializers.ModelSerializer):
    chat_url = serializers.HyperlinkedRelatedField(
        view_name="chat:chat-detail", source='chat', lookup_field='id', read_only=True
    )
    message_url = serializers.HyperlinkedIdentityField(
        view_name="chat:message-detail", source='chat', lookup_field='id', read_only=True
    )
    is_sender_me = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id',
                  'chat',
                  'chat_url',
                  'message_url',
                  'sender',
                  'is_sender_me',
                  'updated',
                  'created']
        extra_kwargs = {
            'sender': {'read_only': True},
        }

    def get_is_sender_me(self, obj):
        request = self.context.get("request")
        user = request.user
        return obj.sender == user

    def validate(self, data):
        data = self._kwargs.get('data')
        chat_id = data.get('chat')
        request = self._kwargs.get('context').get('request')
        user = request.user
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            raise ValidationError("Chat entered does not exist")

        if SoldTimeSlotSale.objects.filter(Q(sold_to=chat.user) & Q(consultant=chat.consultant)).exists():
            if chat.user == user or chat.consultant.user == user:
                return data

        raise ValidationError("You can't access to the chat")

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['sender'] = request.user
        return super(MessageSerializer, self).create(validated_data)


class TextMessageSerializer(MessageSerializer):

    class Meta(MessageSerializer.Meta):
        model = TextMessage
        fields = MessageSerializer.Meta.fields + ['text_message', ]


class VoiceMessageSerializer(MessageSerializer):

    class Meta(MessageSerializer.Meta):
        model = VoiceMessage
        fields = MessageSerializer.Meta.fields + ['voice_field', ]


class FileMessageSerializer(MessageSerializer):

    class Meta(MessageSerializer.Meta):
        model = FileMessage
        fields = MessageSerializer.Meta.fields + ['file_field', ]


class ImageMessageSerializer(MessageSerializer):

    class Meta(MessageSerializer.Meta):
        model = ImageMessage
        fields = MessageSerializer.Meta.fields + ['image_field', ]


class MessagePolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "messageType"
    model_serializer_mapping = {
        Message: MessageSerializer,
        TextMessage: TextMessageSerializer,
        VoiceMessage: VoiceMessageSerializer,
        ImageMessage: ImageMessageSerializer,
        FileMessage: FileMessageSerializer
    }
