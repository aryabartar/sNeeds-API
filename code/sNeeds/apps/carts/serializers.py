from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Cart

from sNeeds.apps.store.serializers import TimeSlotSaleSerializer, SoldTimeSlotSaleSerializer
from sNeeds.apps.store.models import SoldTimeSlotSale, TimeSlotSale, Product
from sNeeds.apps.webinars.models import Webinar
from sNeeds.apps.webinars.serializers import WebinarSerializer, SoldWebinarSerializer
from ..storePackages.models import StorePackage
from ..storePackages.serializers import StorePackageSerializer


class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail", lookup_field='id', read_only=True)
    time_slot_sales = serializers.SerializerMethodField(read_only=True)
    webinars = serializers.SerializerMethodField(read_only=True)
    store_packages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'products', 'time_slot_sales', 'store_packages', 'webinars',
                  'subtotal', 'total', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'time_slot_sales': {'read_only': True},
            'webinars': {'read_only': True},
            'user': {'read_only': True},
            'subtotal': {'read_only': True},
            'total': {'read_only': True},
        }

    def get_time_slot_sales(self, obj):
        time_slot_sales = []

        for product in obj.products.all():
            try:
                time_slot_sale = product.timeslotsale
                time_slot_sales.append(time_slot_sale)
            except TimeSlotSale.DoesNotExist:
                pass

        return TimeSlotSaleSerializer(
            time_slot_sales,
            context=self.context,
            many=True
        ).data

    def get_webinars(self, obj):
        webinars = []
        for product in obj.products.all():
            try:
                webinar_r = product.webinar
                webinars.append(webinar_r)
            except Webinar.DoesNotExist:
                pass

        return WebinarSerializer(
            webinars,
            context=self.context,
            many=True
        ).data

    def get_store_packages(self, obj):
        store_packages = []

        for product in obj.products.all():
            try:
                store_package = product.storepackage
                store_packages.append(store_package)
            except StorePackage.DoesNotExist:
                pass

        return StorePackageSerializer(
            store_packages,
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
        # Validate empty products
        if len(products) == 0:
            raise ValidationError("No products in cart")

        # Validate time conflicts
        products_id = [p.id for p in products]
        products_qs = Product.objects.filter(id__in=products_id)

        time_slot_sales_qs = products_qs.get_time_slot_sales()
        webinars_qs = products_qs.get_webinars()

        for wr in webinars_qs:
            if not wr.active:
                raise ValidationError({"detail": "Webinar is not active"})

        for ts in time_slot_sales_qs:
            conflicting_sold_time_slots = SoldTimeSlotSale.objects.filter(
                sold_to=user,
                start_time__lt=ts.start_time,
                end_time__gt=ts.start_time
            ) | SoldTimeSlotSale.objects.filter(
                sold_to=user,
                start_time__lt=ts.end_time,
                end_time__gt=ts.end_time
            )
            if conflicting_sold_time_slots.exists():
                raise ValidationError({"detail": "Conflict with sold time slot!"})

            time_slot_sales_without_ts_qs = time_slot_sales_qs.exclude(pk=ts.pk)
            conflicting_time_slots = time_slot_sales_without_ts_qs.filter(
                start_time__lt=ts.start_time,
                end_time__gt=ts.start_time
            ) | time_slot_sales_without_ts_qs.filter(
                start_time__lt=ts.end_time,
                end_time__gt=ts.end_time
            )
            if conflicting_time_slots.exists():
                raise ValidationError({"detail": "Conflict with time slot!"})

        return products
