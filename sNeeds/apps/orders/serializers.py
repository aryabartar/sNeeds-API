from rest_framework import serializers

from .models import Order

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.billing.models import BillingProfile


class OrderSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="order:cart-detail", lookup_field='id', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'billing_profile', 'order_id', 'cart', 'status', 'total', 'active', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'billing_profile': {'read_only': True},
            'order_id': {'read_only': True},
            'cart': {'read_only': True},
            'status': {'read_only': True},
            'total': {'read_only': True},
        }

    def validate(self, attrs):
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user

        cart_qs = Cart.objects.filter(user=user, active=True)
        if cart_qs.count() != 1:
            raise serializers.ValidationError({"detail": "User has no active cards."})

        return attrs

    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user

        billing_profile, created = BillingProfile.objects.get_or_create(user=user)
        cart = Cart.objects.get(user=user, active=True)

        order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart)
        return order_obj
