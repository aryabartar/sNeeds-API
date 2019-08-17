from rest_framework import serializers
from .models import TweetModel

from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer


class TweetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="tweets:tweet-detail", lookup_field='id'
    )
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = TweetModel
        fields = [
            'id',
            'url',
            'sender',
            'receiver',
            'file',
            'text',
        ]

    def get_sender(self, obj):
        request = self.context.get("request")
        print(request.data)
        return SafeUserDataSerializer(
            obj.sender, context={"request": request}
        ).data

    def get_receiver(self, obj):
        request = self.context.get("request")
        return SafeUserDataSerializer(
            obj.receiver, context={"request": request}
        ).data


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
