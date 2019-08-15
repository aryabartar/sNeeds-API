
from rest_framework import serializers

from .models import TweetModel


class TextMessageModelSerializerSender(serializers.ModelSerializer):
    class Meta:
        model = TweetModel
        fields = [
            'text',
            'file',
            'sender',
            'receiver',
            ]


class TextMessageModelSerializerReceiver(serializers.ModelSerializer):
    class Meta:
        model = TweetModel
        fields = [
            'id',
            'text',
            'file',
            'sender',
            'receiver',
            'date_created',
            'edited',
            'seen'
            ]
        read_only_fields = ['sender',
                            'date_created',
                            'edited',
                            'seen'
                            ]