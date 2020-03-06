from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import StorePackagePhase, StorePackagePhaseThrough


class StorePackageDetailPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePackagePhase
        fields = ['title', 'price']


class StorePackageDetailPhaseThroughSerializer(serializers.ModelSerializer):
    store_package_detail = serializers.SerializerMethodField()


    class Meta:
        model = StorePackagePhaseThrough
        fields = ['store_package_detail_phase', 'price']

    def get_store_package_field(self, obj):
        return StorePackageDetailPhaseSerializer(obj.store_package_detail).data
