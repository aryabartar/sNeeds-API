from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import StorePackagePhase, StorePackagePhaseThrough


class StorePackagePhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePackagePhase
        fields = ['title', 'price']


class StorePackagePhaseThroughSerializer(serializers.ModelSerializer):
    store_package_phase = serializers.SerializerMethodField()

    class Meta:
        model = StorePackagePhaseThrough
        fields = ['store_package_detail_phase', 'price']

    def get_store_package_phase(self, obj):
        return StorePackagePhaseSerializer(obj.store_package_phase).data
