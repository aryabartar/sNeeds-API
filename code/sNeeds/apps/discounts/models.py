from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import Product

User = get_user_model()


class DiscountManager(models.QuerySet):
    @transaction.atomic
    def new_discount_with_products_users_consultant(self, products, users, consultants, **kwargs):
        obj = self.create(**kwargs)
        obj.products.add(*products)
        obj.users.add(*users)
        obj.consultants.add(*consultants)
        return obj

    @transaction.atomic
    def create_consultant_100_discount(self, consultant, user=None, use_limit=None):
        # obj = Discount(amount=consultant.time_slot_price,
        #     use_limit=use_limit,
        #     creator="consultant",)
        # obj.users.set([user.id])
        # obj.consultants.set([consultant.id])
        # obj.save()

        obj = self.create(
            amount=consultant.time_slot_price,
            use_limit=use_limit,
            creator="consultant",
        )
        obj.users.add(user)
        obj.consultants.add(consultant)
        obj.save()
        return obj


class TimeSlotSaleNumberDiscountModelManager(models.Manager):
    def get_discount_or_zero(self, num):
        try:
            obj = self.get(number=num)
            return obj.discount
        except TimeSlotSaleNumberDiscount.DoesNotExist:
            return 0


class TimeSlotSaleNumberDiscount(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    discount = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    objects = TimeSlotSaleNumberDiscountModelManager()

    def __str__(self):
        return str(self.number)


class CICharField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()


class Discount(models.Model):
    CREATORS = (
        ('consultant', 'Consultant'),
        ('admin', 'Admin'),
    )
    consultants = models.ManyToManyField(ConsultantProfile, blank=True)
    users = models.ManyToManyField(User, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    amount = models.PositiveIntegerField()
    code = CICharField(
        max_length=128, unique=True, blank=True,
        help_text="If want to populate automatically, Leave this field blank. Otherwise enter code"
    )
    use_limit = models.PositiveIntegerField(null=True, blank=True)
    creator = models.CharField(choices=CREATORS, max_length=10, default="admin")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = DiscountManager.as_manager()

    def __str__(self):
        return "{}|{}".format(str(self.amount), str(self.code))

    def update_increase_use_limit(self):
        if self.use_limit is not None:
            self.use_limit = self.use_limit + 1
            self.save()

    def update_decrease_use_limit(self):
        if self.use_limit is not None:
            self.use_limit = self.use_limit - 1
            self.save()


# TODO If a discount that was created by a consultant is being removed, cart discount should be removed too?
# TODO Don't We record discounts created by consultants to discover abuses?


class CartDiscount(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("cart", "discount"),)

    def __str__(self):
        return "cart {} discount".format(str(self.discount))
