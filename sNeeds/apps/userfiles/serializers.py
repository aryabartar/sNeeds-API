from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models

User = get_user_model()


class UserFileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(lookup_field='id', view_name='account:user-file-detail')

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
        if file and file.size > 5242880:
            raise serializers.ValidationError({"detail": "File limit exceeds 5MB."})

        qs = models.UserFile.objects.filter(user=user, type=attrs['type'])

        if request.method == "POST":
            if qs.exists():
                raise serializers.ValidationError({"detail": "User with type should be unique."})

        else:
            if qs.count() > 1:
                raise serializers.ValidationError({"detail": "User with type should be unique."})

        return attrs

    def create(self, validated_data):
        user = self.context.get('request', None).user

        obj = models.UserFile.objects.create(
            user=user,
            file=validated_data['file'],
            type=validated_data['type'],
        )
        return obj
