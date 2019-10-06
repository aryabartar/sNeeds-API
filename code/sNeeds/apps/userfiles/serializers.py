from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from . import models

User = get_user_model()


class UserFileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(lookup_field='id', view_name='userfile:user-file-detail')
    FILE_SIZE_LIMIT = 5242880
    class Meta:
        model = models.UserFile
        fields = ['id', 'url', 'user', 'file', 'type', ]
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def validate(self, attrs):
        file = attrs.get('file', None)
        request = self.context.get('request', None)
        user = request.user

        # ~5MBs
        if file and file.size > self.FILE_SIZE_LIMIT:
            raise serializers.ValidationError({"detail": _("File limit exceeds %(size)d MB.".fromat({"size": self.FILE_SIZE_LIMIT//1000000}))})

        qs = models.UserFile.objects.filter(user=user, type=attrs['type'])

        if request.method == "POST":
            if qs.exists():
                raise serializers.ValidationError({"detail": _("User with already has an resume %(resume)s".format({"resume": qs.first()}))})

        else:
            if qs.count() > 1:
                raise serializers.ValidationError({"detail": _("User with already has an resume %(resume)s".format({"resume": qs.first()}))})

        return attrs

    def create(self, validated_data):
        user = self.context.get('request', None).user

        obj = models.UserFile.objects.create(
            user=user,
            file=validated_data['file'],
            type=validated_data['type'],
        )
        return obj
