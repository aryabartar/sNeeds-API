from django.contrib import admin

from .models import TimeSlotSaleNumberDiscount, Discount, CartDiscount

admin.site.register(TimeSlotSaleNumberDiscount)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('amount',)


@admin.register(CartDiscount)
class CartDiscountAdmin(admin.ModelAdmin):
    list_display = ('cart', 'discount')
