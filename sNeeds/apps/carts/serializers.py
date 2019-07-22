from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail", lookup_field='id', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'time_slot_sales', 'total', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'total': {'read_only': True},
        }

    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user

        cart_qs = Cart.objects.filter(user=user)
        if cart_qs.count() > 0:
            raise ValidationError({"detail": "User has an active cart."})

        time_slot_sales = validated_data.get('time_slot_sales', [])
        cart_obj = Cart.objects.new_cart_with_time_sales(time_slot_sales, user=user)
        return cart_obj
