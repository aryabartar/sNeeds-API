from rest_framework import serializers
from .models import BookletField, BookletTopic, Booklet


class FieldSerializer(serializers.ModelSerializer):
    # topics = serializers.SerializerMethodField()
    #
    # def get_topics(self):
    #

    class Meta:
        model = BookletField
        fields = [
            'title', 'slug',
        ]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookletTopic
        fields = [
            'field', 'title', 'slug'
        ]
