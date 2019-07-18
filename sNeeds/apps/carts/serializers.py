from rest_framework import serializers

from .models import Cart


# TODO : Add time_slot_sales validator for invalid data.
class CartSerializer(serializers.ModelSerializer):
    time_slot_sales = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        lookup_field='id',
        view_name='store:time-slot-sale-detail'
    )

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

        time_slot_sales = request.data.get('time_slot_sales', [])
        cart_obj = Cart.objects.get_new_and_deactive_others(user, time_slot_sales=time_slot_sales)
        return cart_obj
