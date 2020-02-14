from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale

User = get_user_model()


class CartManager(models.QuerySet):
    def remove_product(self, product):
        qs = self._chain()
        for obj in qs:
            obj.time_slot_sales.remove(product)
        return qs

    @transaction.atomic
    def new_cart_with_products(self, products, **kwargs):
        obj = self.create(**kwargs)
        obj.time_slot_sales.add(*products)
        return obj

    @transaction.atomic
    def set_cart_paid(self, cart):
        pass


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    subtotal = models.IntegerField(default=0, blank=True)
    total = models.IntegerField(default=0, blank=True)
    products = models.ManyToManyField(TimeSlotSale, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager.as_manager()

    def get_products_count(self):
        return self.products.all().count()

    def _update_total_cart_consultant_discount_percent(self):
        # from sNeeds.apps.discounts.models import CartConsultantDiscount
        #
        # time_slot_sales = self.products.all()
        # cart_consultant_discount_qs = CartConsultantDiscount.objects.filter(cart__id=self.id)
        # total = 0
        #
        # for t in time_slot_sales:
        #     percent = 0
        #
        #     for obj in cart_consultant_discount_qs:
        #         consultants_qs = obj.consultant_discount.consultant.all()
        #
        #         if t.consultant in consultants_qs:
        #             percent += obj.consultant_discount.percent
        #
        #     total += t.price * ((100.0 - percent) / 100)
        # self.total = total
        pass

    def _update_total_time_slot_number(self):
        # from sNeeds.apps.discounts.models import TimeSlotSaleNumberDiscount
        #
        # time_slot_sale_count = self.get_products_count()
        # count_discount = TimeSlotSaleNumberDiscount.objects.get_discount_or_zero(time_slot_sale_count)
        # self.total = self.total * ((100.0 - count_discount) / 100)
        pass

    def is_acceptable_for_pay(self):
        if self.total > 0:
            return True
        return False

    def _update_total(self):
        # For code discount
        self._update_total_cart_consultant_discount_percent()

        # For quantity discount
        self._update_total_time_slot_number()

    def update_price(self):
        products_qs = self.products.all()
        total = 0
        for product in products_qs:
            total += product.price

        self.subtotal = total
        self._update_total()

        self.save()

    @transaction.atomic
    def set_time_slot_sales(self, products):
        for p in products:
            self.products.add(p)
        self.save()

    def __str__(self):
        return "User {} cart | pk: {}".format(self.user, str(self.pk))
