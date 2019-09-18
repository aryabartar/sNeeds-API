from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CartConsultantDiscount, ConsultantDiscount, TimeSlotSaleNumberDiscount


class TimeSlotSaleNumberDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlotSaleNumberDiscount
        fields = ['number', 'discount', ]


class ConsultantDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantDiscount
        fields = ['consultant', 'percent', ]


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
        fields = ['id', 'consultant_discount', 'url', 'code', ]

    def get_consultant_discount(self, obj):
        consultant_discount_serialize = ConsultantDiscountSerializer(obj.consultant_discount)
        return consultant_discount_serialize.data

    def validate_code(self, code):
        consultant_discount = ConsultantDiscount.objects.get_with_code_or_none(code)
        if consultant_discount is None:
            raise ValidationError({"detail": "Code is not valid"})
        if not consultant_discount.active:
            raise ValidationError({"detail": "Code is not valid",
                                   "detail_fa": "این کد نامعتبر است"})
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

        # Checking that if entered code wasn't in the database throws a ValidationError
        try:
            ConsultantDiscount.objects.get(code=code)
        except ConsultantDiscount.DoesNotExist:
            raise ValidationError({"detail": "This discount doesn't exist."})

        # Checking that user has bought a session with the code's consultant or not
        discount_consultant = ConsultantDiscount.objects.get(code=code).consultant.all()
        exist = False
        for consultant in discount_consultant:
            for time in cart.time_slot_sales.all():
                if time.consultant == consultant:
                    exist = True
                    break
            if exist:
                break
        if not exist:
            raise ValidationError({"detail": "You don't have any session with the consultants of discount"})

        # Checking that user cannot use multiple discounts for a consultant
        applied_discount = CartConsultantDiscount.objects.filter(cart=cart).values_list('consultant_discount',
                                                                                        flat=True)
        unused_discount_consultants = ConsultantDiscount.objects.get(code=code).consultant
        for discount_id in applied_discount:
            applied_discount_consultants = list(ConsultantDiscount.objects.get(id=discount_id).consultant.all())
            for consultant in applied_discount_consultants:
                if unused_discount_consultants.filter(id=consultant.id):
                    raise ValidationError({
                        "detail": "You already have used a discount for consultant " + str(consultant.id),
                        "detail_fa": "شما هم اکنون برای مشاور " +
                                     str(consultant.id) +
                                     " کد تخفیف استفاده کرده اید."
                    })

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
