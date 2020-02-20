from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import CartConsultantDiscount, ConsultantDiscount, TimeSlotSaleNumberDiscount


class TimeSlotSaleNumberDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlotSaleNumberDiscount
        fields = ['number', 'discount', ]


class ConsultantDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantDiscount
        fields = ['consultants', 'percent', ]


class CartConsultantDiscountSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        source="consultant_discount.code",
        required=True, max_length=128
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="discount:cart-consultant-discount-detail",
        lookup_field='id'
    )
    consultant_discount = serializers.SerializerMethodField()

    class Meta:
        model = CartConsultantDiscount
        fields = ['id', 'cart', 'consultant_discount', 'url', 'code', ]

    def get_consultant_discount(self, obj):
        consultant_discount_serialize = ConsultantDiscountSerializer(obj.consultant_discount)
        return consultant_discount_serialize.data

    def validate_code(self, code):
        # Checking that code is valid and active
        try:
            ConsultantDiscount.objects.get(code__iexact=code, active=True)
        except ConsultantDiscount.DoesNotExist:
            raise ValidationError(_("Code is not valid"))

        return code

    def validate(self, attrs):
        cart = attrs.get("cart")

        # Checking that discount is applied in the cart
        qs = CartConsultantDiscount.objects.filter(cart=cart, )
        if qs.exists():
            raise ValidationError(_("This cart has an active code"))

        # Checking that user has bought a session with the code's consultant or not
        discount = ConsultantDiscount.objects.get(code=attrs.get("consultant_discount").get("code"))
        discount_consultants_id = list(discount.consultants.all().values_list('id', flat=True))
        cart_products_consultants_id = list(
            cart.products.all().get_time_slot_sales().values_list('consultant', flat=True)
        )
        if len(list(set(discount_consultants_id) & set(cart_products_consultants_id))):
            raise ValidationError(_("There is no product in cart that this discount can apply to."))

        return attrs

    def create(self, validated_data):
        code = validated_data.get("consultant_discount", {}).get('code')
        try:
            consultant_discount = ConsultantDiscount.objects.get(code__iexact=code)
        except ConsultantDiscount.DoesNotExist:
            consultant_discount = None

        obj = CartConsultantDiscount.objects.create(
            cart=validated_data.get("cart"),
            consultant_discount=consultant_discount
        )

        return obj
