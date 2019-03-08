from rest_framework import serializers

from .models import Cart

from classes.serializers import PublicClassSerializer


class CartSerializer(serializers.ModelSerializer):
    public_classes = serializers.SerializerMethodField()

    def get_public_classes(self, cart):
        public_classes = cart.public_classes.all()
        public_classes_serialize = PublicClassSerializer(public_classes, many=True)
        return public_classes_serialize.data

    class Meta:
        model = Cart
        fields = "__all__"
