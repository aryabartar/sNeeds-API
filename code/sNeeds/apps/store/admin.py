from django.contrib import admin
from .models import TimeSlotSale, SoldTimeSlotSale, Product

admin.site.register(Product)
admin.site.register(SoldTimeSlotSale)


@admin.register(TimeSlotSale)
class StorePackageAdmin(admin.ModelAdmin):
    readonly_fields = ["price", "active", ]

