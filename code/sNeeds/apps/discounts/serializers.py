from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import CartDiscount, Discount, TimeSlotSaleNumberDiscount


class TimeSlotSaleNumberDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlotSaleNumberDiscount
        fields = ['number', 'discount', ]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['consultants', 'webinars', 'amount', ]


class CartDiscountSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        source="discount.code",
        required=True, max_length=128
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="discount:cart-discount-detail",
        lookup_field='id'
    )
    discount = serializers.SerializerMethodField()

    class Meta:
        model = CartDiscount
        fields = ['id', 'cart', 'discount', 'url', 'code', ]

    def get_discount(self, obj):
        discount_serialize = DiscountSerializer(obj.discount)
        return discount_serialize.data

    def validate_code(self, code):
        # Checking that code is valid and active
        try:
            Discount.objects.get(code__iexact=code)
        except Discount.DoesNotExist:
            raise ValidationError(_("Code is not valid"))

        return code

    def validate(self, attrs):
        cart = attrs.get("cart")

        # Checking that discount is applied in the cart
        qs = CartDiscount.objects.filter(cart=cart, )
        if qs.exists():
            raise ValidationError(_("This cart has an active code"))

        # Checking that user has bought a session with the code's consultant or not
        discount = Discount.objects.get(code=attrs.get("discount").get("code"))
        discount_consultants_id = list(discount.consultants.all().values_list('id', flat=True))
        discount_webinars_id = list(discount.webinars.all().values_list('id', flat=True))
        cart_products_consultants_id = list(
            cart.products.all().get_time_slot_sales().values_list('consultant', flat=True)
        )
        cart_products_webinars_id = list(
            cart.products.all().get_webinars().values_list('id', flat=True)
        )

        if len(list(set(discount_consultants_id) & set(cart_products_consultants_id))) == 0 and \
                len(list(set(discount_webinars_id) & set(cart_products_webinars_id))) == 0:
            raise ValidationError(_("There is no product in cart that this discount can apply to."))

        return attrs

    def create(self, validated_data):
        code = validated_data.get("discount", {}).get('code')
        try:
            discount = Discount.objects.get(code__iexact=code)
        except Discount.DoesNotExist:
            discount = None

        obj = CartDiscount.objects.create(
            cart=validated_data.get("cart"),
            discount=discount
        )

        return obj
