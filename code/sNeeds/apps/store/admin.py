from django.contrib import admin
from .models import TimeSlotSale, SoldTimeSlotSale, Product
from advanced_filters.admin import AdminAdvancedFiltersMixin

admin.site.register(Product)


@admin.register(TimeSlotSale)
class TimeSlotSaleAdmin(admin.ModelAdmin):
    list_display = ["id", "consultant", "start_time", "end_time", "price"]
    readonly_fields = ["price", "active", ]


class SoldTimeSlotSaleAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ["id", "consultant", "start_time", "end_time", "sold_to", "price"]
    list_filter = ('consultant',)
    search_fields = ["id", ]
    advanced_filter_fields =  [
        "created"
    ]


admin.site.register(SoldTimeSlotSale, SoldTimeSlotSaleAdmin)
