from django.contrib import admin

from .models import TimeSlotSaleNumberDiscount, Discount, CartDiscount

admin.site.register(TimeSlotSaleNumberDiscount)


@admin.register(Discount)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('percent',)


@admin.register(CartDiscount)
class CartConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('cart', 'discount',)
