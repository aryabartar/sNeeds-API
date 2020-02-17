from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Cart

from sNeeds.apps.store.serializers import TimeSlotSaleSerializer, SoldTimeSlotSaleSerializer
from sNeeds.apps.store.models import SoldTimeSlotSale, TimeSlotSale, Product


class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail", lookup_field='id', read_only=True)
    time_slot_sales = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'products', 'time_slot_sales',
                  'subtotal', 'total', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'time_slot_sales': {'read_only': True},
            'user': {'read_only': True},
            'subtotal': {'read_only': True},
            'total': {'read_only': True},
        }

    def get_time_slot_sales(self, obj):
        time_slot_sales = []
        for product in obj.products.all():
            if isinstance(product, TimeSlotSale):
                time_slot_sales.append(product.timeslotsale)

        return TimeSlotSaleSerializer(
            time_slot_sales,
            context=self.context,
            many=True
        ).data

    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user

        # self.super.create
        products = validated_data.get('products', [])
        cart_obj = Cart.objects.new_cart_with_products(products, user=user)
        return cart_obj

    def validate_products(self, products):
        user = self.context.get('request').user

        products_id = [p.id for p in products]
        products_qs = Product.objects.filter(id__in=products_id)

        print(products_qs)
        time_slot_sales_qs = products_qs.get_time_slot_sales()
        print(time_slot_sales_qs)
        # for ts in time_slot_sales_list:
        #     conflicting_sold_time_slots = SoldTimeSlotSale.objects.filter(
        #         sold_to=user,
        #         start_time__lt=ts.start_time,
        #         end_time__gt=ts.start_time
        #     ) | SoldTimeSlotSale.objects.filter(
        #         sold_to=user,
        #         start_time__lt=ts.end_time,
        #         end_time__gt=ts.end_time
        #     )
        #
        #     if conflicting_sold_time_slots.exists():
        #         raise ValidationError({"detail": "Conflict with sold time slot!"})

            # print(products_qs)
        # for i in range(len(time_slot_sales_list)):
        #     if (
        #             sold_time_slots.filter(
        #                 start_time__lt=time_slot_sales_list[i].start_time).filter(
        #                 end_time__gt=time_slot_sales_list[i].start_time)
        #             or
        #             sold_time_slots.filter(
        #                 start_time__lt=time_slot_sales_list[i].end_time).filter(
        #                 end_time__gt=time_slot_sales_list[i].end_time)
        #     ):
        #         raise ValidationError(
        #             {"detail": _(
        #                 "Time Conflict between %(selected_time_slot)d and %(sold_time_slot)d which is a bought session" % {
        #                     "selected_time_slot": time_slot_sales_list[i].id,
        #                     "sold_time_slot": sold_time_slots.first().id}),
        #                 "selected_time_slot": time_slot_sales_list[i].id,
        #                 "sold_time_slot": sold_time_slots.first().id
        #             }
        #         )
        #
        #     for j in range(i + 1, len(time_slot_sales_list)):
        #         if time_slot_sales_list[j].start_time < time_slot_sales_list[i].start_time < time_slot_sales_list[
        #             j].end_time \
        #                 or list_of_sessions[j].start_time < time_slot_sales_list[i].end_time < time_slot_sales_list[
        #             j].end_time:
        #             raise ValidationError(
        #                 {
        #                     "detail": _(
        #                         "Time Conflict between %(selected_time_slot_1)d and %(selected_time_slot_2)d" % {
        #                             "selected_time_slot_1": time_slot_sales_list[i].id,
        #                             "selected_time_slot_2": time_slot_sales_list[j].id}),
        #                     "selected_time_slot_1": time_slot_sales_list[i].id,
        #                     "selected_time_slot_2": time_slot_sales_list[j].id
        #                 }
        #             )

        return products
