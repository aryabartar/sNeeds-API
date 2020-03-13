from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from ..store.serializers import SoldTimeSlotSaleSerializer
from ..webinars.serializers import SoldWebinarSerializer


class OrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="order:order-detail", lookup_field='id', read_only=True)
    sold_time_slot_sales = serializers.SerializerMethodField()
    used_consultant_discount = serializers.SerializerMethodField()
    sold_webinars = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'url', 'order_id', 'status', 'subtotal', 'total', 'sold_time_slot_sales', 'created', 'updated',
                  'used_consultant_discount', 'time_slot_sales_number_discount', 'sold_webinars']

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

    def get_sold_webinars(self, obj):
        sold_webinars = obj.sold_products.all().get_sold_webinars()
        return SoldWebinarSerializer(
            sold_webinars, many=True, context={"request": self.context.get("request")}
        ).data

    def get_used_consultant_discount(self, obj):
        if obj.used_consultant_discount is None:
            return None
        else:
            return {
                "code": obj.used_consultant_discount.code,
                "percent": obj.used_consultant_discount.percent
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
