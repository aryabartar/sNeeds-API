from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    other_name = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id', 'other_name'
        ]

    def get_other_name(self, obj):
        request = self.context.get('request')
        user = request.user

        if user == obj.user:
            return obj.consultant.user.get_full_name()

        return obj.user.get_full_name()
