from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order, SoldOrder

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer, SoldCartSerializer


class OrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="order:order-detail", lookup_field='id', read_only=True)
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'url', 'order_id', 'cart', 'status', 'total', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'order_id': {'read_only': True},
            'status': {'read_only': True},
            'total': {'read_only': True},
        }

    def validate(self, attrs):
        user = self.context.get('request', None).user

        order_qs = Order.objects.filter(cart__user=user)
        if order_qs.count() > 0:
            raise ValidationError({"detail": "User has an active order."})

        return attrs

    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except:
            raise ValidationError({"detail": _("User has no cart.")})

        order_obj = Order.objects.create(cart=cart)

        return order_obj


class SoldOrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="order:sold-order-detail", lookup_field='id', read_only=True)
    cart = SoldCartSerializer(read_only=True)

    class Meta:
        model = SoldOrder
        fields = ['id', 'url', 'order_id', 'cart', 'status', 'total', 'created', 'updated', ]
