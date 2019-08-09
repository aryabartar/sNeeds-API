from django.contrib import admin

from .models import TimeSlotSaleNumberDiscount, ConsultantDiscount, CartConsultantDiscount

admin.site.register(TimeSlotSaleNumberDiscount)


@admin.register(ConsultantDiscount)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('percent', 'start', 'end')


@admin.register(CartConsultantDiscount)
class CartConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('cart', 'consultant_discount',)
