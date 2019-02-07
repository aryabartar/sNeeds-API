from rest_framework import serializers
from .models import Post, UserComment, Topic, HelloModel


# serializes Post objects
class PostSerializer(serializers.ModelSerializer):
    # post_url = serializers.SerializerMethodField()
    #
    # def get_post_url(self, post):
    #     """
    #     This method returns a complete url for a topic.
    #     """
    #     request = self.context.get('request')
    #     topic_url = post.get_absolute_url()
    #     return request.build_absolute_uri(topic_url)

    class Meta:
        model = Post
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    topic_url = serializers.SerializerMethodField()  # Will use 'get_topic_url' method

    def get_topic_url(self, topic):
        """
        This method returns a complete url for a topic.
        """
        request = self.context.get('request')
        topic_url = topic.get_absolute_url()
        return request.build_absolute_uri(topic_url)

    class Meta:
        model = Topic
        fields = [
            'title',
            'slug',
            'topic_url',
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


class PostCommentsSerializer(serializers.Serializer):
    """
    This serializer is used to serialize comments for a post.
    In other words UserComment and AdminComments are combined together.
    """
    username = serializers.CharField(max_length=80)
    comment = serializers.CharField(max_length=1000)
    admin_name = serializers.CharField(max_length=80)
    admin_answer = serializers.CharField(max_length=1000)


class HelloSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelloModel
        fields = '__all__'
