from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ConsultantComment, ConsultantAdminComment, SoldTimeSlotRate
from ..customAuth.serializers import SafeUserDataSerializer


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="comments:comment-detail", lookup_field='id', read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    admin_reply = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConsultantComment
        fields = ['id', 'url', 'user', 'admin_reply', 'consultant', 'message', 'created', 'updated', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }

    def get_admin_reply(self, obj):
        try:
            admin_reply = ConsultantAdminComment.objects.get(comment=obj)
            return admin_reply.message
        except ConsultantAdminComment.DoesNotExist:
            return None

    def get_user(self, obj):
        return SafeUserDataSerializer(obj.user).data

    def validate(self, attrs):
        request = self.context.get("request", None)
        user = request.user

        if not request:
            raise ValidationError({"detail": _("Request is None")})

        if not user:
            raise ValidationError({"detail": _("User is None.")})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = request.user

        obj = ConsultantComment.objects.create(
            user=user,
            consultant=validated_data['consultant'],
            message=validated_data['message'],
        )

        return obj


class AdminCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantAdminComment
        fields = ['id', 'comment', 'message', 'created', 'updated', ]


class SoldTimeSlotRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldTimeSlotRate
        fields = ['id', 'sold_time_slot', 'rate', ]

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = request.user

        sold_time_slot = validated_data['sold_time_slot']

        if sold_time_slot.sold_to != user:
            raise ValidationError({"detail": _("This time slot is not sold to this user")})

        obj = SoldTimeSlotRate.objects.create(
            sold_time_slot=sold_time_slot,
            rate=validated_data['rate'],
        )

        return obj
