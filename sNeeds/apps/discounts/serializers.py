from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CartConsultantDiscount


class CartConsultantDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartConsultantDiscount
        fields = ['consultant_discount']

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = request.user

        try:
            cart = user.cart
        except:
            raise ValidationError("User has no cart.")

        obj = CartConsultantDiscount.objects.create_with_consultant_discount(
            validated_data["consultant_discount"],
            cart=cart,
        )

        return obj
