from django.contrib import admin

from .models import TimeSlotSaleNumberDiscount, ConsultantDiscount

admin.site.register(TimeSlotSaleNumberDiscount)


@admin.register(ConsultantDiscount)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('percent', 'start', 'end')
