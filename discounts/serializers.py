from rest_framework import serializers
from .models import Cafe, CafeImage


class CafeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeImage
        fields = [
            'image',
        ]


class CafeSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, cafe):
        all_images = cafe.images
        return CafeImageSerializer(all_images, many=True).data

    class Meta:
        model = Cafe
        fields = [
            'name', 'information', 'address', 'phone_number', 'slug',
            'images',
        ]
