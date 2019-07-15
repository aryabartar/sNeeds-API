from rest_framework import serializers

from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'time_slot_sales', 'total']
        extra_kwargs = {
            'id': {'read_only': True},
            'total': {'read_only': True},
        }

    def validate(self, data):
        if len(Cart.objects.filter(user__id=data.get('user').id)) > 0:
            raise serializers.ValidationError("This user already has cart.")
        return data
