from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import StorePackageDetailPhase


class StorePackageDetailPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePackageDetailPhase
        fields = ['title', 'price']

