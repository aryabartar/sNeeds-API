from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CartConsultantDiscount


class CartConsultantDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartConsultantDiscount
        fields = ['id', 'consultant_discount']

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = request.user

        try:
            cart = user.cart
        except:
            raise ValidationError("User has no cart.")

        obj = CartConsultantDiscount.objects.create(cart=cart, **validated_data)

        return obj
