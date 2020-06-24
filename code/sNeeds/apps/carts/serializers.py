from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Cart

from sNeeds.apps.store.serializers import TimeSlotSaleSerializer, SoldTimeSlotSaleSerializer
from sNeeds.apps.store.models import SoldTimeSlotSale, TimeSlotSale, Product
from sNeeds.apps.basicProducts.models import BasicProduct, ClassProduct, WebinarProduct
from sNeeds.apps.basicProducts.serializers import BasicProductSerializer, SoldBasicProductSerializer, \
    ClassProductSerializer, WebinarProductSerializer
from ..storePackages.models import StorePackage, SoldStoreUnpaidPackagePhase
from ..storePackages.serializers import StorePackageSerializer, SoldStoreUnpaidPackagePhaseSerializer


class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail", lookup_field='id', read_only=True)
    time_slot_sales = serializers.SerializerMethodField(read_only=True)
    class_products = serializers.SerializerMethodField(read_only=True)
    webinar_products = serializers.SerializerMethodField(read_only=True)
    store_packages = serializers.SerializerMethodField(read_only=True)
    sold_store_unpaid_package_phases = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'products',
                  'time_slot_sales', 'store_packages', 'class_products', 'webinar_products',
                  'sold_store_unpaid_package_phases',
                  'subtotal', 'total', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'time_slot_sales': {'read_only': True},
            'class_products': {'read_only': True},
            'webinar_products': {'read_only': True},
            'store_packages': {'read_only': True},
            'sold_store_unpaid_package_phases': {'read_only': True},
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

    def get_class_products(self, obj):
        class_products = []

        for product in obj.products.all():
            try:
                class_product = ClassProduct.objects.get(pk=product.id)
                class_products.append(class_product)
            except ClassProduct.DoesNotExist:
                pass

        return ClassProductSerializer(
            class_products,
            context=self.context,
            many=True,
        ).data

        # basic_products = []
        #
        # for product in obj.products.all():
        #     try:
        #         basic_product = product.basicproduct
        #         basic_products.append(basic_product)
        #     except BasicProduct.DoesNotExist:
        #         pass
        #
        # return BasicProductSerializer(
        #     basic_products,
        #     context=self.context,
        #     many=True
        #  ).data

    def get_webinar_products(self, obj):
        webinar_products = []
        for product in obj.products.all():
            try:
                webinar_product = WebinarProduct.objects.get(pk=product.id)
                webinar_products.append(webinar_product)
            except WebinarProduct.DoesNotExist:
                pass

        return WebinarProductSerializer(
            webinar_products,
            context=self.context,
            many=True,
        ).data

        # basic_products = []
        #
        # for product in obj.products.all():
        #     try:
        #         basic_product = product.basicproduct
        #         basic_products.append(basic_product)
        #     except BasicProduct.DoesNotExist:
        #         pass
        #
        # return BasicProductSerializer(
        #     basic_products,
        #     context=self.context,
        #     many=True
        # ).data

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

    def get_sold_store_unpaid_package_phases(self, obj):
        sold_store_unpaid_package_phases = []

        for product in obj.products.all():
            try:
                sold_store_unpaid_package_phase = product.soldstoreunpaidpackagephase
                sold_store_unpaid_package_phases.append(sold_store_unpaid_package_phase)
            except SoldStoreUnpaidPackagePhase.DoesNotExist:
                pass

        return SoldStoreUnpaidPackagePhaseSerializer(
            sold_store_unpaid_package_phases,
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
        basic_products_qs = products_qs.get_basic_products()

        for bp in basic_products_qs:
            if not bp.active:
                raise ValidationError({"detail": "basic product is not active"})

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
