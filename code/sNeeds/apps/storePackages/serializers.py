from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import StorePackagePhase, StorePackagePhaseThrough, StorePackage, ConsultantSoldStorePackageAcceptRequest, \
    SoldStorePackage, SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase, SoldStorePackagePhaseDetail
from ..consultants.models import ConsultantProfile
from ..customAuth.serializers import SafeUserDataSerializer


class StorePackagePhaseThroughSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name='store-package:store-package-phase-through-detail',
    )
    store_package = serializers.HyperlinkedRelatedField(
        lookup_field='slug',
        read_only=True,
        view_name='store-package:store-package-detail'
    )
    title = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = StorePackagePhaseThrough
        fields = ['id', 'url', 'title', 'store_package', 'phase_number', 'price']

    def get_title(self, obj):
        return obj.store_package_phase.title

    def get_price(self, obj):
        return obj.store_package_phase.price


class StorePackageSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='slug',
        view_name='store-package:store-package-detail',
    )

    store_package_phases = serializers.HyperlinkedRelatedField(
        lookup_field='id',
        many=True,
        read_only=True,
        view_name='store-package:store-package-phase-through-detail'
    )

    class Meta:
        model = StorePackage
        fields = ['url', "price", "total_price", "active", "title", "store_package_phases", ]


class ConsultantSoldStorePackageAcceptRequestSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name='store-package:consultant-sold-store-package-accept-request-detail'
    )

    class Meta:
        model = ConsultantSoldStorePackageAcceptRequest
        fields = ['id', 'url', 'sold_store_package', 'consultant', 'created', 'updated']


class SoldStorePackageSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name='store-package:sold-store-package-detail'
    )
    sold_to = serializers.SerializerMethodField()
    consultant = serializers.HyperlinkedRelatedField(
        lookup_field='slug',
        read_only=True,
        view_name='consultant:consultant-profile-detail'
    )

    class Meta:
        model = SoldStorePackage
        fields = ['url', 'title', 'sold_to', 'consultant', 'paid_price', 'total_price', 'created', 'updated']
        extra_kwargs = {
            'title': {'read_only': True},
            'sold_to': {'read_only': True},
            'paid_price': {'read_only': True},
            'total_price': {'read_only': True},
        }

    def get_sold_to(self, obj):
        return SafeUserDataSerializer(obj.sold_to).data


class SoldStorePackagePhaseSerializer(serializers.ModelSerializer):
    sold_store_package = serializers.HyperlinkedRelatedField(
        lookup_field='id',
        read_only=True,
        view_name='store-package:sold-store-package-detail'
    )

    class Meta:
        fields = ['title', 'detailed_title', 'price', 'sold_store_package', 'phase_number', 'status']
        extra_kwargs = {
            'url': {'read_only': True},
            'title': {'read_only': True},
            'detailed_title': {'read_only': True},
            'price': {'read_only': True},
            'sold_store_package': {'read_only': True},
            'phase_number': {'read_only': True},
            'status': {'read_only': True},
        }


class SoldStoreUnpaidPackagePhaseSerializer(SoldStorePackagePhaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name='store-package:sold-store-unpaid-package-phase-detail'
    )

    class Meta(SoldStorePackagePhaseSerializer.Meta):
        fields = SoldStorePackagePhaseSerializer.Meta.fields + ['url']
        model = SoldStoreUnpaidPackagePhase


class SoldStorePaidPackagePhaseSerializer(SoldStorePackagePhaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name='store-package:sold-store-paid-package-phase-detail'
    )

    class Meta(SoldStorePackagePhaseSerializer.Meta):
        fields = SoldStorePackagePhaseSerializer.Meta.fields + ['url', 'consultant_done']
        model = SoldStorePaidPackagePhase


class SoldStorePackagePhaseRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, SoldStorePaidPackagePhase):
            return 'hello'
        elif isinstance(value, SoldStoreUnpaidPackagePhase):
            return 'hi'
        raise Exception('Unexpected type of SoldStorePackagePhase object')


# TODO: FILTER! In list!
class SoldStorePackagePhaseDetailSerializer(SoldStorePackagePhaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name='store-package:sold-store-package-phase-detail-detail'
    )
    consultant = serializers.PrimaryKeyRelatedField(queryset=ConsultantProfile.objects.all())
    content_object = SoldStorePackagePhaseRelatedField(read_only=True)

    class Meta:
        model = SoldStorePackagePhaseDetail
        fields = ['url', 'status', 'created', 'updated', 'consultant', 'content_type', 'object_id', 'content_object']
        extra_kwargs = {
            'content_object': {'read_only': True},
            'consultant': {'write_only': True},
        }


    def validate(self, attrs):
        consultant = attrs.pop('consultant')
        # if consultant ==
        # print(attrs.get("content_type").objects.get(id='object_id'))
        print(attrs.get("content_type"))
        return attrs

    def create(self, validated_data):
        try:
            super().create(validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
