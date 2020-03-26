from rest_framework import serializers
from .models import BasicProduct, SoldBasicProduct
from ..customAuth.serializers import SafeUserDataSerializer


class BasicProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasicProduct
        fields = ('id', 'title', 'slug', 'active', 'price')

        extra_kwargs = {
            'id': {'read_only': True},
            'slug': {'read_only': True},
        }


class SoldBasicProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name="basic-product:sold-basic-product-detail",
        read_only=True
    )

    basic_product = serializers.HyperlinkedRelatedField(
        read_only=True,
        lookup_field='slug',
        view_name='basic-product:basic-product-detail'
    )

    sold_to = serializers.SerializerMethodField()

    class Meta:
        model = SoldBasicProduct
        fields = [
            'id', 'url', 'basic_product', 'price', 'sold_to',
        ]

    def get_sold_to(self, obj):
        return SafeUserDataSerializer(obj.sold_to).data
