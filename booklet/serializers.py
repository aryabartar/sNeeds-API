from rest_framework import serializers
from .models import BookletField, BookletTopic, Booklet


class FieldSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    field_url = serializers.SerializerMethodField()

    def get_field_url(self, field):
        """ This method returns a complete url for a field. """
        request = self.context.get('request')
        field_url = field.get_absolute_url()
        return request.build_absolute_uri(field_url)

    def get_topics(self, field):
        all_field_topics = field.topics.all()
        return TopicSerializer(all_field_topics, many=True, context=self.context).data

    class Meta:
        model = BookletField
        fields = [
            'title', 'field_url', 'slug', 'topics'
        ]


class TopicSerializer(serializers.ModelSerializer):
    field = serializers.SerializerMethodField()
    topic_url = serializers.SerializerMethodField()

    def get_topic_url(self, topic):
        request = self.context.get('requst')
        topic_url = topic.get_absolute_url()
        return request.build_absolute_uri(topic_url)

    def get_field(self, topic):
        return topic.field.title

    class Meta:
        model = BookletTopic
        fields = [
            'field', 'title', 'topic_url', 'slug'
        ]
