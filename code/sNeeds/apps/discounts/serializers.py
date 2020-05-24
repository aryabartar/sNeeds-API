from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from .models import CartDiscount, Discount, TimeSlotSaleNumberDiscount
from ..store.models import Product
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer
from sNeeds.apps.consultants.serializers import ShortConsultantProfileSerializer

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


# class UsersField(serializers.Field):
#
#     def to_representation(self, value):
#         return SafeUserDataSerializer(value.users, many=True).data
#
#     def to_internal_value(self, data):
#         ret = {
#             "users": data["users"]['id'],
#         }
#         return ret


class DiscountSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        source='discounts',
        lookup_field='id',
        view_name='discount:consultant-discount-detail',
        read_only=True
    )

    is_used = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Discount
        fields = ['id', 'consultants', 'products', 'amount', 'code', 'users', 'created', 'updated', 'use_limit', 'url',
                  'is_used']
        extra_kwargs = {
            'consultants': {'read_only': True},
            'products': {'read_only': True},
            'amount': {'read_only': True},
            'code': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'use_limit': {'read_only': True},
            'is_used': {'read_only': True},
            'url': {'read_only': True},
        }

    def get_is_used(self, obj):
        if obj.use_limit is not None:
            if obj.use_limit == 0:
                return True
            else:
                return False
        return False

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

        if discount.use_limit is not None:
            if discount.use_limit < 1:
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


class ConsultantInteractiveUsersSerializer(serializers.Serializer):

    interact_users = serializers.SerializerMethodField(read_only=True)
    consultant = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_interact_users(self, obj):
        from sNeeds.apps.consultants.models import ConsultantProfile
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user
        consultant_profile = ConsultantProfile.objects.get(user__id=user.id)

        users = get_users_interact_with_consultant(consultant_profile)
        return SafeUserDataSerializer(users, many=True, context=self.context).data

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_consultant(self, obj):
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user
        consultant_profile = ConsultantProfile.objects.get(user=user)
        return ShortConsultantProfileSerializer(consultant_profile, context=self.context).data

