from django.contrib import admin

from .models import TimeSlotSaleNumberDiscount, Discount, CartDiscount

admin.site.register(TimeSlotSaleNumberDiscount)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'use_limit', 'amount', 'creator', 'created')
    list_filter = ('creator',)
    filter_horizontal = ["consultants", "users", "products"]


@admin.register(CartDiscount)
class CartDiscountAdmin(admin.ModelAdmin):
    list_display = ('cart', 'discount')
