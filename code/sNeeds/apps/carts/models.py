from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale, Product

User = get_user_model()


class CartManager(models.QuerySet):
    def remove_product(self, product):
        qs = self._chain()
        for obj in qs:
            obj.products.remove(product)
        return qs

    @transaction.atomic
    def new_cart_with_products(self, products, **kwargs):
        obj = self.create(**kwargs)
        obj.products.add(*products)
        return obj

    @transaction.atomic
    def update_price(self):
        qs = self._chain()
        for obj in qs:
            obj.update_price()
        return qs


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.IntegerField(default=0, blank=True)
    total = models.IntegerField(default=0, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager.as_manager()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        from sNeeds.apps.consultants.models import ConsultantProfile
        if ConsultantProfile.objects.filter(user=self.user).exists():
            raise ValidationError({
                "user": "Cart user can not be a consultant.",
            })

    def get_time_slot_sales_count(self):
        return self.products.all().get_time_slot_sales().count()

    def _update_total_cart_discount_percent(self):
        from sNeeds.apps.discounts.models import CartDiscount

        products = self.products.all()
        try:
            cart_discount = CartDiscount.objects.get(cart__id=self.id)
        except CartDiscount.DoesNotExist:
            self.total = self.subtotal
            return

        total = 0
        for product in products:
            percent = 0

            # For TimeSlots
            try:
                time_slot_sale = product.timeslotsale  # Checks here
                consultants_qs = cart_discount.discount.consultants.all()
                if time_slot_sale.consultant in consultants_qs:
                    percent += cart_discount.discount.percent
            except TimeSlotSale.DoesNotExist:
                pass

            total += product.price * ((100.0 - percent) / 100)
        self.total = total

    def _update_total_time_slot_number(self):
        from sNeeds.apps.discounts.models import TimeSlotSaleNumberDiscount

        time_slot_sale_count = self.get_time_slot_sales_count()
        count_discount = TimeSlotSaleNumberDiscount.objects.get_discount_or_zero(time_slot_sale_count)

        self.total = self.total * ((100.0 - count_discount) / 100)

    def is_acceptable_for_pay(self):
        if self.total > 0:
            return True
        return False

    def _update_total(self):
        # For code discount
        self._update_total_cart_discount_percent()

        # For quantity discount
        self._update_total_time_slot_number()

    def update_price(self):
        products_qs = self.products.all()
        subtotal = 0
        for product in products_qs:
            subtotal += product.price

        self.subtotal = subtotal
        self._update_total()

        self.save()

    @transaction.atomic
    def set_time_slot_sales(self, products):
        for p in products:
            self.products.add(p)
        self.save()

    def __str__(self):
        return "User {} cart | pk: {}".format(self.user, str(self.pk))
