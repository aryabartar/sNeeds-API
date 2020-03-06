from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import StorePackagePhase, StorePackagePhaseThrough


class StorePackagePhaseThroughSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    store_package_phase = serializers.SerializerMethodField()

    class Meta:
        model = StorePackagePhaseThrough
        fields = ['title', 'store_package', 'order', 'price']

    def get_title(self, obj):
        return obj.store_package_phase.title

    def get_price(self, obj):
        return obj.store_package_phase.price
