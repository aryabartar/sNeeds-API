from os.path import basename

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_polymorphic.serializers import PolymorphicSerializer

from sNeeds.apps.store.models import SoldTimeSlotSale
from sNeeds.apps.consultants.models import ConsultantProfile
from .models import Chat, Message, TextMessage, VoiceMessage, FileMessage, ImageMessage


class ChatSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="chat:chat-detail", lookup_field='id')
    other_person = serializers.SerializerMethodField()
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id',
            'url',
            'other_person',
            'profile_img',
            'created',
            'updated',
        ]

    def get_profile_img(self, obj):
        request = self.context.get("request")
        user = request.user
        consultant = obj.consultant

        if user == consultant.user:
            return None

        elif consultant.profile_picture:
            profile_img = consultant.profile_picture.url
            return request.build_absolute_uri(profile_img)

        else:
            return None

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
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id',
                  'chat',
                  'chat_url',
                  'message_url',
                  'sender',
                  'tag',
                  'is_sender_me',
                  'updated',
                  'created',
                  'profile_img']
        extra_kwargs = {
            'sender': {'read_only': True},
            'tag': {'read_only': True}
        }

    def get_is_sender_me(self, obj):
        request = self.context.get("request")
        user = request.user
        return obj.sender == user

    def get_profile_img(self, obj):
        request = self.context.get("request")

        if obj.sender.is_consultant():
            consultant_profile = ConsultantProfile.objects.get(user=obj.sender)
            if consultant_profile.profile_picture:
                profile_img = consultant_profile.profile_picture.url
                return request.build_absolute_uri(profile_img)
        else:
            return None

    def validate(self, data):
        data = self._kwargs.get('data')
        chat_id = data.get('chat')
        request = self._kwargs.get('context').get('request')
        user = request.user
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            raise ValidationError("Chat entered does not exist")

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
    name = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()

    class Meta(MessageSerializer.Meta):
        model = VoiceMessage
        fields = MessageSerializer.Meta.fields + ['voice_field',
                                                  'name',
                                                  'volume']

    def get_name(self, obj):
        try:
            file = obj.voice_field.file
            return basename(file.name)
        except FileNotFoundError as ex:
            return ex.strerror

    def get_volume(self, obj):
        try:
            return obj.voice_field.size
        except FileNotFoundError as ex:
            return ex.strerror


class FileMessageSerializer(MessageSerializer):
    name = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()

    class Meta(MessageSerializer.Meta):
        model = FileMessage
        fields = MessageSerializer.Meta.fields + ['file_field',
                                                  'name',
                                                  'volume']

    def get_name(self, obj):
        try:
            file = obj.file_field.file
            return basename(file.name)
        except FileNotFoundError as ex:
            return ex.strerror

    def get_volume(self, obj):
        try:
            return obj.file_field.size
        except FileNotFoundError as ex:
            return ex.strerror


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
