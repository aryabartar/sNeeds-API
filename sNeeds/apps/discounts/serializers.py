from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CartConsultantDiscount, ConsultantDiscount


class ConsultantDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantDiscount
        fields = ['consultant', 'percent', ]


class CartConsultantDiscountSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        source="consultant_discount.code",
        required=True, max_length=128
    )
    url = serializers.HyperlinkedIdentityField(view_name="discount:cart-consultant-discount-detail", lookup_field='id')
    consultant_discount = serializers.SerializerMethodField()

    class Meta:
        model = CartConsultantDiscount
        fields = ['id', 'consultant_discount', 'url', 'code', ]

    def get_consultant_discount(self, obj):
        consultant_discount_serialize = ConsultantDiscountSerializer(obj.consultant_discount)
        return consultant_discount_serialize.data

    def validate_code(self, code):
        consultant_discount = ConsultantDiscount.objects.get_with_code_or_none(code)
        if consultant_discount is None:
            raise ValidationError({"detail": "Code is not valid"})
        return code

    def validate(self, attrs):
        request = self.context.get("request", None)
        user = request.user

        try:
            cart = user.cart
        except:
            raise ValidationError({"detail": "User has no cart."})

        code = attrs.get("consultant_discount", {}).get('code')
        qs = CartConsultantDiscount.objects.filter(cart=cart, consultant_discount__code=code)

        if qs.exists():
            raise ValidationError({"detail": "This discount is already used in this cart"})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = request.user

        code = validated_data.get("consultant_discount", {}).get('code')
        consultant_discount = ConsultantDiscount.objects.get_with_code_or_none(code)

        cart = user.cart

        obj = CartConsultantDiscount.objects.create(
            cart=cart,
            consultant_discount=consultant_discount
        )

        return obj
