from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from ..store.serializers import SoldTimeSlotSaleSerializer


class OrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="order:order-detail", lookup_field='id', read_only=True)
    sold_time_slot_sales = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'url', 'order_id', 'status', 'subtotal', 'total', 'sold_time_slot_sales', 'created', 'updated',
                  'used_consultant_discount', 'time_slot_sales_number_discount', ]

        extra_kwargs = {
            'id': {'read_only': True},
            'order_id': {'read_only': True},
            'status': {'read_only': True},
            'used_consultant_discount': {'read_only': True},
            'time_slot_sales_number_discount': {'read_only': True},
            'subtotal': {'read_only': True},
            'total': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }

    def get_sold_time_slot_sales(self, obj):
        sold_time_slot_sales = obj.sold_products.all().get_sold_time_slot_sales()
        return SoldTimeSlotSaleSerializer(
            sold_time_slot_sales, many=True, context={"request": self.context.get("request")}
        ).data

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
