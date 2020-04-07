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

        # Consultant can't create cart
        if ConsultantProfile.objects.filter(user=self.user).exists():
            raise ValidationError({
                "user": "Cart user can not be a consultant.",
            })

        # Due to this problem products active status is validated in many to many signal
        # https://stackoverflow.com/questions/7986510/django-manytomany-model-validation

    def get_time_slot_sales_count(self):
        return self.products.all().get_time_slot_sales().count()

    def get_basic_products_count(self):
        return self.products.all().get_basic_products().count()

    def _update_total_cart_no_discount_code_or_deleted(self):
        # If user doesn't use code discount we wanna he be able to use our non code discounts
        from sNeeds.apps.discounts.models import TimeSlotSaleNumberDiscount

        time_slots_sales = self.products.all().get_time_slot_sales()

        time_slots_sales_price = 0
        for time_slots_sale in time_slots_sales:
            time_slots_sales_price += time_slots_sale.price

        time_slot_sale_count = self.get_time_slot_sales_count()
        count_discount = TimeSlotSaleNumberDiscount.objects.get_discount_or_zero(time_slot_sale_count)

        self.total = self.total - (count_discount * time_slots_sales_price) / 100

    def _update_total_cart_discount_amount(self):
        from sNeeds.apps.discounts.models import CartDiscount
        from sNeeds.apps.discounts.models import TimeSlotSaleNumberDiscount

        products = self.products.all()
        try:
            cart_discount = CartDiscount.objects.get(cart__id=self.id)
        except CartDiscount.DoesNotExist:
            self.total = self.subtotal
            self._update_total_cart_no_discount_code_or_deleted()
            return

        discount = cart_discount.discount

        # Consultants that are in the discount of code entered
        consultants_qs = cart_discount.discount.consultants.all()

        # Products that are in the discount of code entered
        products_qs = cart_discount.discount.products.all()

        # For apply time slot number discount
        time_slot_sale_count = self.get_time_slot_sales_count()

        # If discount is given by one consultant to one user we remove one time slot from products
        # and also consultant from consultants , so no other time slots will be affected by discount
        # but count discount will remain with one fewer time slots
        if discount.creator == "consultant":
            discount_creator_time_slot_qs = \
                self.products.all().get_time_slot_sales().filter(consultant__in=consultants_qs)

            if discount_creator_time_slot_qs.exists():
                discount_creator_first_time_slot_id = discount_creator_time_slot_qs.first().id
                products = self.products.all().exclude(id=discount_creator_first_time_slot_id)
                consultants_qs = consultants_qs.none()
                time_slot_sale_count -= 1

        count_discount = TimeSlotSaleNumberDiscount.objects.get_discount_or_zero(time_slot_sale_count)

        total = 0
        for product in products:
            effective_price = 0

            # For TimeSlots
            try:
                time_slot_sale = product.timeslotsale  # Checks here

                # If user applied discount code we apply num discount for lower price
                if time_slot_sale.consultant in consultants_qs:
                    effective_price = product.price - cart_discount.discount.amount
                else:
                    effective_price = product.price

                effective_price = effective_price * ((100.0 - count_discount) / 100)
                if effective_price < 0:
                    effective_price = 0
                total += effective_price
                continue
            except TimeSlotSale.DoesNotExist:
                pass

            # For products
            if product in products_qs:
                effective_price = product.price - cart_discount.discount.amount
                if effective_price < 0:
                    effective_price = 0
            else:
                effective_price = product.price

            total += effective_price
        self.total = total

    def is_acceptable_for_pay(self):
        if self.total > 0:
            return True
        return False

    def _update_total(self):
        # For code discount and time slot number discount
        self._update_total_cart_discount_amount()

    def update_price(self):
        products_qs = self.products.all()
        subtotal = 0
        for product in products_qs:
            subtotal += product.price

        self.subtotal = subtotal
        self._update_total()

        self.save()

    def update_products(self):
        products_qs = self.products.all()

        for product in products_qs:
            if not product.active:
                self.products.remove(product)
        self.save()

    @transaction.atomic
    def set_time_slot_sales(self, products):
        for p in products:
            self.products.add(p)
        self.save()

    @transaction.atomic
    def set_basic_products(self, products):
        for p in products:
            self.products.add(p)
        self.save()

    def __str__(self):
        return "User {} cart | pk: {}".format(self.user, str(self.pk))
