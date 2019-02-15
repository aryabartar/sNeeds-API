from rest_framework import serializers
from .models import Cafe, CafeImage, Discount, UserDiscount


class CafeImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, image):
        request = self.context.get('request')
        image_url = image.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = CafeImage
        fields = [
            'image_url',
        ]


class CafeSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    discounts = serializers.SerializerMethodField()

    def get_discounts(self, cafe):
        all_cafe_discounts = cafe.discounts
        return DiscountSerializerInfo(all_cafe_discounts, many=True).data

    def get_url(self, cafe):
        request = self.context.get('request')
        cafe_url = cafe.get_absolute_url()
        return request.build_absolute_uri(cafe_url)

    def get_images(self, cafe):
        all_images = cafe.images
        return CafeImageSerializer(all_images, many=True, context=self.context).data

    class Meta:
        model = Cafe
        fields = [
            'id', 'name', 'information', 'address', 'phone_number',
            'url', 'slug', 'images', 'discounts'
        ]


class DiscountSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'id', 'discount_percent', 'discount_info',
        ]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class UserDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDiscount
        fields = [
            'discount', 'user', 'code',
        ]
        read_only_fields = [
            'user', 'code',
        ]
