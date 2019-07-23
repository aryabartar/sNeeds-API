from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Comment, AdminComment


class CommentSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="comments:comment-detail", lookup_field='id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'url', 'user', 'first_name', 'consultant', 'message', 'created', 'updated', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }

    def get_first_name(self, obj):
        return obj.user.get_short_name()

    def validate(self, attrs):
        request = self.context.get("request", None)
        user = request.user

        if not request:
            raise ValidationError({"detail": "Request is None"})

        if not user:
            raise ValidationError({"detail": "Authentication credentials are not provided."})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = request.user

        obj = Comment.objects.create(
            user=user,
            consultant=validated_data['consultant'],
            message=validated_data['message'],
        )

        return obj


class AdminCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminComment
        fields = ['id', 'comment', 'message', 'created', 'updated', ]
