from rest_framework import serializers

from .models import PublicClass


class PublicClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicClass
        fields = "__all__"
