from rest_framework import serializers
from .models import BookletField, BookletTopic, Booklet


class FieldSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()

    def get_topics(self, field):
        all_field_topics = field.topics.all()
        return TopicSerializer(all_field_topics, many=True, context=self.context).data

    class Meta:
        model = BookletField
        fields = [
            'title', 'slug', 'topics'
        ]


class TopicSerializer(serializers.ModelSerializer):
    field = serializers.SerializerMethodField()
    # field_url = serializers.SerializerMethodField()

    def get_field(self, topic):
        return topic.field.title

    class Meta:
        model = BookletTopic
        fields = [
            'field', 'title', 'slug'
        ]
