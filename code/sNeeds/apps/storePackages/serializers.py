from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

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

    store_package_phases = serializers.SerializerMethodField()

    class Meta:
        model = StorePackage
        fields = ["id", 'url', "slug", "price", "total_price", "active", "title", "store_package_phases", ]

    def get_store_package_phases(self, obj):
        return StorePackagePhaseThroughSerializer(
            StorePackagePhaseThrough.objects.filter(store_package=obj),
            context={"request": self.context.get("request")},
            many=True
        ).data


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
        fields = ['id', 'url', 'title', 'sold_to', 'consultant', 'paid_price', 'total_price', 'created', 'updated']
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


class ContentTypeRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return ContentType.objects.filter(app_label='storePackages', model='soldstorepaidpackagephase') | \
               ContentType.objects.filter(app_label='storePackages', model='soldstoreunpaidpackagephase')

    def to_internal_value(self, data):
        if data == 'soldstorepaidpackagephase':
            return ContentType.objects.get(app_label='storePackages', model='soldstorepaidpackagephase')
        elif data == 'soldstoreunpaidpackagephase':
            return ContentType.objects.get(app_label='storePackages', model='soldstoreunpaidpackagephase')
        else:
            raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)

    def to_representation(self, value):
        if value.model_class() == SoldStorePaidPackagePhase:
            return 'soldstorepaidpackagephase'
        elif value.model_class() == SoldStoreUnpaidPackagePhase:
            return 'soldstoreunpaidpackagephase'
        else:
            raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)


# TODO: FILTER! In list!
class SoldStorePackagePhaseDetailSerializer(SoldStorePackagePhaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name='store-package:sold-store-package-phase-detail-detail'
    )
    content_type = ContentTypeRelatedField()

    class Meta:
        model = SoldStorePackagePhaseDetail
        fields = ['id', 'url', 'title', 'status', 'created', 'updated', 'content_type', 'object_id', ]
        extra_kwargs = {
            'content_object': {'read_only': True},
        }

    def validate(self, attrs):
        user = self.context.get('request').user
        consultant = ConsultantProfile.objects.get(user=user)

        try:
            content_object = attrs.get("content_type").model_class().objects.get(id=attrs.get('object_id'))
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError(e)

        if consultant != content_object.sold_store_package.consultant:
            raise PermissionDenied(
                {"detail": "Consultant has no permission to SoldStorePackagePhaseDetail."},
            )
        return attrs
