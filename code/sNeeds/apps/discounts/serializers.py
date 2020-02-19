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
        fields = ['id', 'consultant_discount','cart', 'url', 'code', ]

    def get_consultant_discount(self, obj):
        consultant_discount_serialize = ConsultantDiscountSerializer(obj.consultant_discount)
        return consultant_discount_serialize.data

    def validate_code(self, code):
        request = self.context.get("request", None)
        user = request.user
        # Checking that user already has a card
        try:
            cart = user.cart
        except:
            raise ValidationError(_("User has no cart."))

        # Checking that the discount user entered is valid or not
        # Checking that code is exist or is active
        try:
            discount = ConsultantDiscount.objects.get(code__iexact=code)
        except ConsultantDiscount.DoesNotExist:
            raise ValidationError(_("Code is not valid"))

        if not discount.active:
            raise ValidationError(_("Code is not valid"))

        # Checking that discount is applied in the cart
        qs = CartConsultantDiscount.objects.filter(cart=cart, consultant_discount__code__iexact=code)
        if qs.exists():
            raise ValidationError(_("This discount is already used in this cart"))

        # Checking that user has bought a session with the code's consultant or not
        discount_consultant = discount.consultant.all()
        exist = False
        for consultant in discount_consultant:
            for time in cart.time_slot_sales.all():
                if time.consultant == consultant:
                    exist = True
                    break
            if exist:
                break

        if not exist:
            raise ValidationError(_("You don't have any session with the consultants of discount"))

        # Checking that user cannot use multiple discounts for a consultant
        applied_discount = CartConsultantDiscount.objects.filter(cart=cart).values_list('consultant_discount',
                                                                                        flat=True)
        for id in applied_discount:
            applied_discount_consultants = list(ConsultantDiscount.objects.get(id=id).consultant.all())
            for consultant in applied_discount_consultants:
                if discount.consultant.filter(id=consultant.id):
                    raise ValidationError({
                        "detail": _(
                            "You already have used a discount for consultant %(number)d " % {'number': consultant.id}),
                        "consultant_id": consultant.id
                    }
                    )

        return code

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = request.user

        code = validated_data.get("consultant_discount", {}).get('code')
        try:
            consultant_discount = ConsultantDiscount.objects.get(code__iexact=code)
        except ConsultantDiscount.DoesNotExist:
            consultant_discount = None

        cart = user.cart

        obj = CartConsultantDiscount.objects.create(
            cart=cart,
            consultant_discount=consultant_discount
        )

        return obj
