from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.discounts.models import ConsultantDiscount, CartConsultantDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.store.models import SoldProduct

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)


class OrderManager(models.Manager):
    @transaction.atomic
    def sell_cart_create_order(self, cart):
        cart_products = cart.products.all()
        time_slot_sales_qs = cart_products.get_time_slot_sales()
        sold_time_slot_sales_qs = time_slot_sales_qs.set_time_slot_sold(sold_to=cart.user)

        try:
            used_discount = CartConsultantDiscount.objects.get(cart=cart)
        except CartConsultantDiscount.DoesNotExist:
            used_discount = None

        try:
            time_slot_sales_number_discount = TimeSlotSaleNumberDiscount.objects.get(
                cart.get_time_slot_sales_count()
            )
        except TimeSlotSaleNumberDiscount.DoesNotExist:
            time_slot_sales_number_discount = 0

        order = Order(
            user=cart.user,
            status='paid',
            total=cart.total,
            subtotal=cart.subtotal,
            used_discount=used_discount,
            time_slot_sales_number_discount=time_slot_sales_number_discount
        )

        order.save()
        order.sold_products.set(sold_time_slot_sales_qs)

        cart.delete()
        return order


class Order(models.Model):
    order_id = models.CharField(max_length=12, blank=True,
                                help_text="Leave this field blank, this will populate automatically.")
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    status = models.CharField(max_length=256, default='paid', choices=ORDER_STATUS_CHOICES)
    sold_products = models.ManyToManyField(SoldProduct, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    used_discount = models.ForeignKey(ConsultantDiscount, null=True, on_delete=models.SET_NULL)
    time_slot_sales_number_discount = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    objects = OrderManager()

    def get_user(self):
        return self.cart.user

    def __str__(self):
        return "Order: {} | pk: {} ".format(str(self.order_id), str(self.pk))
