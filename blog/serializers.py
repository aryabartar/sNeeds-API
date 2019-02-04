from rest_framework import serializers
from .models import Post, UserComment, Topic


# serializes Post objects
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'topic',
            'updated',
            'timestamp',
        ]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'title',
            'slug',
        ]


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = [
            'user',
            'content',
            'post',
        ]

    # validates content data
    def validate_content(self, value):
        if len(value) > 200:
            raise serializers.ValidationError("This comment is long!")
        return value
