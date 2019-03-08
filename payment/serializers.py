from rest_framework import serializers

from .models import Cart


# from classes.

# from classes.models import P

class CartSerializer(serializers.ModelSerializer):
    public_classes = serializers.SerializerMethodField()

    def get_public_classes(self, cart):
        public_classes = cart.public_classes.all()
        # public_classes_serialize =

    class Meta:
        model = Cart
        fields = "__all__"
