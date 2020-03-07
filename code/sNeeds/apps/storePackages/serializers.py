from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import StorePackagePhase, StorePackagePhaseThrough, StorePackage


class StorePackagePhaseThroughSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='store-package:store-package-phase-through-detail',
        lookup_field='id'
    )
    title = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = StorePackagePhaseThrough
        fields = ['url', 'title', 'store_package', 'phase_number', 'price']

    def get_title(self, obj):
        return obj.store_package_phase.title

    def get_price(self, obj):
        return obj.store_package_phase.price


class StorePackageSerializer(serializers.ModelSerializer):
    first_price = serializers.IntegerField(source='price')
    total_price = serializers.SerializerMethodField()
    store_package_phases = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='store-package:store-package-phase-through-detail'
    )

    class Meta:
        model = StorePackage
        fields = ["title", "store_package_phases", "slug", "first_price", "total_price"]

    def get_total_price(self, obj):
        qs = StorePackagePhaseThrough.objects.filter(store_package=obj)
        total = 0
        for obj in qs:
            total += obj.store_package_phase.price
        return total
