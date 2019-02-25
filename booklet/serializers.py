from rest_framework import serializers
from .models import BookletField, BookletTopic, Booklet, Tag


class FieldSerializer(serializers.ModelSerializer):
    field_url = serializers.SerializerMethodField()

    def get_field_url(self, field):
        """ This method returns a complete url for a field. """
        request = self.context.get('request')
        field_url = field.get_absolute_url()
        return request.build_absolute_uri(field_url)

    class Meta:
        model = BookletField
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    topic_url = serializers.SerializerMethodField()

    def get_topic_url(self, topic):
        request = self.context.get('request')
        topic_url = topic.get_absolute_url()
        return request.build_absolute_uri(topic_url)

    class Meta:
        model = BookletTopic
        fields = "__all__"


class BookletSerializer(serializers.ModelSerializer):
    booklet_url = serializers.SerializerMethodField()

    def get_booklet_url(self, booklet):
        request = self.context.get('request')
        booklet_url = booklet.get_absolute_url()
        return request.build_absolute_uri(booklet_url)

    class Meta:
        model = Booklet
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    tag_url = serializers.SerializerMethodField()

    def get_tag_url(self, tag):
        request = self.context.get('request')
        tag_url = tag.get_absolute_url()
        return request.build_absolute_uri(tag_url)

    class Meta:
        model = Tag
        fields = "__all__"
