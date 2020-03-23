from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import CartDiscount, Discount, TimeSlotSaleNumberDiscount
from .utils import unique_discount_code_generator
from ..consultants.models import ConsultantProfile
from ..store.models import Product


class TimeSlotSaleNumberDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlotSaleNumberDiscount
        fields = ['number', 'discount', ]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['consultants', 'products', 'amount', 'code', 'users']
        extra_kwargs = {
            'consultant': {'read_only': True},
            'products': {'read_only': True},
            'amount': {'read_only': True},
            'code': {'read_only': True}
        }

    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if len(validated_data['products']) != 0:
            raise ValidationError("No products in cart")

        if validated_data.get('users', None) is None:
            raise ValidationError("No students defined to use discount")

        consultant_profile = ConsultantProfile.objects.get(user=user)
        consultants = validated_data.get('consultants', [])
        consultants.add(consultant_profile)



        users = validated_data.get('users', [])
        products = validated_data.get('products', [])

        code = unique_discount_code_generator()
        amount = validated_data.get('amount')

        obj = Discount.objects.new_discount_with_products_and_users_and_consultant(products, users, consultants,
                                                                                   code=code, amount=amount,
                                                                                   )






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

        discount = Discount.objects.get(code=attrs.get("discount").get("code"))

        # Checking that user has bought a session with the code's consultant or not
        discount_consultants_id = list(discount.consultants.all().values_list('id', flat=True))
        cart_products_consultants_id = list(
            cart.products.all().get_time_slot_sales().values_list('consultant', flat=True)
        )

        # Checking that user has bought a session with the code's product or not
        discount_products_id = list(discount.products.all().values_list('id', flat=True))
        cart_products_id = list(
            cart.products.all().values_list('id', flat=True)
        )

        if len(list(set(discount_consultants_id) & set(cart_products_consultants_id))) == 0 and \
                len(list(set(discount_products_id) & set(cart_products_id))) == 0:
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
