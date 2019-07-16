from rest_framework import serializers

from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'time_slot_sales', 'total']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'total': {'read_only': True},
        }

    def validate(self, data):
        request = self.context.get("request", None)
        user = request.user
        if not user.is_authenticated:
            raise serializers.ValidationError({"detail": "User is not authenticated."})

        return data

    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user
        qs = Cart.objects.filter(user=user)
        if qs.exists():
            raise serializers.ValidationError({"detail": "Cart already exists."})

        cart_obj = Cart(
            user=user
        )
        cart_obj.save()
        for time_slot_sale in validated_data['time_slot_sales']:
            cart_obj.time_slot_sales.add(time_slot_sale)
        cart_obj.save()
        return cart_obj
