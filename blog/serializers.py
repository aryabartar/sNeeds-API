from rest_framework import serializers
from .models import Post


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
