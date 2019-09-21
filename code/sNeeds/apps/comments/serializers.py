from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Comment, AdminComment, SoldTimeSlotRate
from sNeeds.apps.store.models import SoldTimeSlotSale


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="comments:comment-detail", lookup_field='id', read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    admin_reply = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'url', 'user', 'admin_reply', 'first_name', 'consultant', 'message', 'created', 'updated', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }

    def get_admin_reply(self, obj):
        admin_reply = None
        try:
            admin_reply = AdminComment.objects.get(comment=obj)
        except:
            pass

        if not admin_reply:
            return None

        return AdminCommentSerializer(admin_reply).data

    def get_first_name(self, obj):
        return obj.user.get_short_name()

    def validate(self, attrs):
        request = self.context.get("request", None)
        user = request.user

        if not request:
            raise ValidationError({"detail": _("Request is None")})

        if user.is_anonymous:
            raise ValidationError({"detail": _("Authentication credentials are not provided.")})

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


class SoldTimeSlotRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldTimeSlotRate
        fields = ['sold_time_slot', 'rate', ]

    def validate(self, attrs):
        request = self.context.get('request', None)
        user = request.user

        sold_time_slot = attrs['sold_time_slot']

        if sold_time_slot.sold_to != user:
            raise ValidationError({"detail": _("This time slot is not sold to this user")})

        return attrs

    def create(self, validated_data):
        sold_time_slot = validated_data['sold_time_slot']

        if SoldTimeSlotRate.objects.filter(sold_time_slot=sold_time_slot).exists():
            raise ValidationError({"detail": _("Rate exists")})

        obj = SoldTimeSlotRate.objects.create(
            sold_time_slot=sold_time_slot,
            rate=validated_data['rate'],
        )

        return obj
