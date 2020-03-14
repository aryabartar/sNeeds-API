from django.contrib import admin

from .models import TimeSlotSaleNumberDiscount, Discount, CartConsultantDiscount

admin.site.register(TimeSlotSaleNumberDiscount)


@admin.register(Discount)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('percent',)


@admin.register(CartConsultantDiscount)
class CartConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('cart', 'consultant_discount',)
