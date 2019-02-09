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
        return TopicSerializerWhitNoBooklet(all_field_topics, many=True, context=self.context).data

    class Meta:
        model = BookletField
        fields = [
            'title', 'field_url', 'slug', 'topics'
        ]


class TopicSerializerWhitNoBooklet(serializers.ModelSerializer):
    field = serializers.SerializerMethodField()
    topic_url = serializers.SerializerMethodField()
    field_url = serializers.SerializerMethodField()

    def get_field_url(self, topic):
        request = self.context.get('request')
        field_url = topic.field.get_absolute_url()
        return request.build_absolute_uri(field_url)

    def get_topic_url(self, topic):
        request = self.context.get('request')
        topic_url = topic.get_absolute_url()
        return request.build_absolute_uri(topic_url)

    def get_field(self, topic):
        return topic.field.title

    class Meta:
        model = BookletTopic
        fields = [
            'title', 'topic_url', 'field', 'field_url', 'slug',
        ]


class TopicSerializer(TopicSerializerWhitNoBooklet):
    topic_booklets = serializers.SerializerMethodField()

    def get_topic_booklets(self, topic):
        topic_booklets = topic.booklets.all()
        topic_booklets_serialize = BookletSerializer(topic_booklets, many=True, context=self.context)
        return topic_booklets_serialize.data


class BookletSerializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    topic_slug = serializers.SerializerMethodField()
    topic_url = serializers.SerializerMethodField()
    field = serializers.SerializerMethodField()
    field_slug = serializers.SerializerMethodField()
    field_url = serializers.SerializerMethodField()

    def get_topic(self, booklet):
        return booklet.topic.title

    def get_topic_slug(self, booklet):
        return booklet.topic.slug

    def get_topic_url(self, booklet):
        request = self.context.get('request')
        booklet_url = booklet.topic.get_absolute_url()
        return request.build_absolute_uri(booklet_url)

    def get_field(self, booklet):
        return booklet.topic.field.title

    def get_field_slug(self, booklet):
        return booklet.topic.field.slug

    def get_field_url(self, booklet):
        request = self.context.get('request')
        field_url = booklet.topic.field.get_absolute_url()
        return request.build_absolute_uri(field_url)

    class Meta:
        model = Booklet
        fields = [
            'title', 'information', 'teacher', 'slug',
            'booklet_content', 'booklet_image', 'topic',
            'topic_slug', 'topic_url', 'field', 'field_slug',
            'field_url',
        ]
