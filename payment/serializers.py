from rest_framework import serializers

from .models import Cart


# from classes.models import P

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
