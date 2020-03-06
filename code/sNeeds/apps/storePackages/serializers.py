from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import StorePackagePhase, StorePackagePhaseThrough


class (serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='store-package:store-package-phase-through-detail',
        lookup_field='id'
    )
    title = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = StorePackagePhaseThrough
        fields = ['url','title', 'store_package', 'phase_number', 'price']

    def get_title(self, obj):
        return obj.store_package_phase.title

    def get_price(self, obj):
        return obj.store_package_phase.price
