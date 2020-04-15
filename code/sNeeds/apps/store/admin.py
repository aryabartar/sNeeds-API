from django.contrib import admin
from .models import TimeSlotSale, SoldTimeSlotSale, Product

admin.site.register(Product)


@admin.register(TimeSlotSale)
class TimeSlotSaleAdmin(admin.ModelAdmin):
    list_display = ["id", "consultant", "start_time", "end_time", "price"]
    readonly_fields = ["price", "active", ]


@admin.register(SoldTimeSlotSale)
class SoldTimeSlotSaleAdmin(admin.ModelAdmin):
    list_display = ["id", "consultant", "start_time", "end_time", "sold_to", "price"]
    readonly_fields = ["price",  ]
