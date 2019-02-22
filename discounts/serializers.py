from rest_framework import serializers
from .models import Cafe, CafeImage, Discount, UserDiscount, CafeProfile, UserDiscountArchive


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

    def get_url(self, cafe):
        request = self.context.get('request')
        cafe_url = cafe.get_absolute_url()
        return request.build_absolute_uri(cafe_url)

    def get_images(self, cafe):
        all_images = cafe.images.all()
        return CafeImageSerializer(all_images, many=True, context=self.context).data

    class Meta:
        model = Cafe
        fields = [
            'id', 'name', 'information', 'address', 'phone_number',
            'url', 'slug', 'images',
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
        read_only_fields = [
            'cafe',
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        cafe_profile = CafeProfile.objects.filter(user__exact=user)
        if not cafe_profile.exists():
            raise serializers.ValidationError("User is not cafe admin.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cafe_profile = CafeProfile.objects.get(user__exact=user)
        cafe = cafe_profile.cafe
        validated_data['cafe'] = cafe
        return Discount.objects.create(**validated_data)


class UserDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDiscount
        fields = "__all__"
        read_only_fields = [
            'user', 'code', 'status',
        ]

# class UserDiscountArchiveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model =