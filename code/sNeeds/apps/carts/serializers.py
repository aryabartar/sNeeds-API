from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Cart

from sNeeds.apps.store.serializers import TimeSlotSaleSerializer, SoldTimeSlotSaleSerializer
from sNeeds.apps.store.models import SoldTimeSlotSale


class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail", lookup_field='id', read_only=True)
    time_slot_sales_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'time_slot_sales', 'time_slot_sales_detail',
                  'subtotal', 'total', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'subtotal': {'read_only': True},
            'total': {'read_only': True},
        }

    def get_time_slot_sales_detail(self, obj):
        return TimeSlotSaleSerializer(
            obj.time_slot_sales,
            context=self.context,
            many=True
        ).data

    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user

        time_slot_sales = validated_data.get('time_slot_sales', [])
        cart_obj = Cart.objects.new_cart_with_time_sales(time_slot_sales, user=user)
        return cart_obj

    def validate_time_slot_sales(self, list_of_sessions):
        sold_slots = SoldTimeSlotSale.objects.filter(sold_to=self.context.get('request').user).filter(used=False)
        for i in range(len(list_of_sessions)):
            if (sold_slots.filter(start_time__lt=list_of_sessions[i].start_time).filter(
                    end_time__gt=list_of_sessions[i].start_time)
                    or sold_slots.filter(start_time__lt=list_of_sessions[i].end_time).filter(
                        end_time__gt=list_of_sessions[i].end_time)):
                raise ValidationError(
                    {"detail": _(
                        "Time Conflict between %(selected_time_slot)d and %(sold_time_slot)d which is a bought session" % {
                            "selected_time_slot": list_of_sessions[i].id, "sold_time_slot": sold_slots.first().id}),
                     "selected_time_slot": list_of_sessions[i].id,
                     "sold_time_slot": sold_slots.first().id
                     }
                )

            for j in range(i + 1, len(list_of_sessions)):
                if list_of_sessions[j].start_time < list_of_sessions[i].start_time < list_of_sessions[j].end_time \
                        or list_of_sessions[j].start_time < list_of_sessions[i].end_time < list_of_sessions[j].end_time:
                    raise ValidationError(
                        {
                            "detail": _(
                                "Time Conflict between %(selected_time_slot_1)d and %(selected_time_slot_2)d" % {
                                    "selected_time_slot_1": list_of_sessions[i].id,
                                    "selected_time_slot_2": list_of_sessions[j].id}),
                            "selected_time_slot_1": list_of_sessions[i].id,
                            "selected_time_slot_2": list_of_sessions[j].id
                        }
                    )
        return list_of_sessions
