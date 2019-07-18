from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'billing_profile', 'order_id', 'cart', 'status', 'total']
        extra_kwargs = {
            'id': {'read_only': True},
            'billing_profile': {'read_only': True},
            'order_id': {'read_only': True},
            'cart': {'read_only': True},
            'status': {'read_only': True},
            'total': {'read_only': True},
        }

    # def create(self, validated_data):
    #     user = self.context.get()
    #
    #     obj = Order(bil)
