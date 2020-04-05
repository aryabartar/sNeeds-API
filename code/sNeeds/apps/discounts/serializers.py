from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from .models import CartDiscount, Discount, TimeSlotSaleNumberDiscount
from ..store.models import Product
from sNeeds.apps.consultants.models import ConsultantProfile

from sNeeds.utils.custom.custom_functions import get_users_interact_with_consultant


User = get_user_model()


class TimeSlotSaleNumberDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlotSaleNumberDiscount
        fields = ['number', 'discount', ]


class ShortDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['consultants', 'products']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'consultants', 'products', 'amount', 'code', 'users']
        extra_kwargs = {
            'consultants': {'read_only': True},
            'products': {'read_only': True},
            'amount': {'read_only': True},
            'code': {'read_only': True},
        }

    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return attrs

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        consultant_profile = ConsultantProfile.objects.get(user=user)
        consultants = [consultant_profile]

        users = validated_data.get('users', [])

        if len(users) == 0:
            raise ValidationError("No students defined to use discount")

        if len(users) > 1:
            raise ValidationError("Give discount to more than one user is not allowed")

        users_are_consultants_qs = ConsultantProfile.objects.filter(user__in=users)
        if users_are_consultants_qs.exists():
            raise ValidationError("No Consultant allowed to be in users")

        users_id = [u.id for u in users]

        interactive_users_qs = get_users_interact_with_consultant(consultant_profile)

        allowed_users = interactive_users_qs.filter(id__in=users_id)

        if not allowed_users.exists():
            raise ValidationError("There is no user that is allowed to get discount code")

        products = []

        obj = Discount.objects.new_discount_with_products_users_consultant(products, users, consultants,
                                                                           amount=consultant_profile.time_slot_price,
                                                                           use_limit=1, creator="consultant",
                                                                           )
        return obj


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
        discount_serialize = ShortDiscountSerializer(obj.discount)
        return discount_serialize.data

    def validate_code(self, code):
        # Checking that code is valid and active
        try:
            Discount.objects.get(code__iexact=code)
        except Discount.DoesNotExist:
            raise ValidationError(_("Code is not valid"))

        return code

    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        cart = attrs.get("cart")

        # Checking that discount is applied in the cart
        qs = CartDiscount.objects.filter(cart=cart, )
        if qs.exists():
            raise ValidationError(_("This cart has an active code"))

        if cart.user != user:
            raise ValidationError(_("The user wants to apply code is not cart owner"))

        discount = Discount.objects.get(code=attrs.get("discount").get("code"))

        use_limit = 0
        if discount.use_limit is not None:
            use_limit = discount.use_limit
            if use_limit > 0:
                use_limit -= 1
            else:
                raise ValidationError(_("Discount has reached to limit"))

        # Checking that if discount has users , cart user is included in discount users
        if discount.users.all().count() > 0:
            qs = discount.users.filter(id=user.id)
            if qs.exists() is not True:
                raise ValidationError(_("The user is not allowed to use this code"))

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

        if discount.use_limit is not None:
            discount.use_limit = use_limit
        discount.save()
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
