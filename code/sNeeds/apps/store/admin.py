from django.contrib import admin
from .models import TimeSlotSale, SoldTimeSlotSale, Product, SoldTimeSlotSalePaymentInfo
from advanced_filters.admin import AdminAdvancedFiltersMixin

from ..orders.models import Order

admin.site.register(Product)


@admin.register(TimeSlotSale)
class TimeSlotSaleAdmin(admin.ModelAdmin):
    list_display = ["id", "consultant", "start_time", "end_time", "price"]
    readonly_fields = ["price", "active", ]


class SoldTimeSlotSaleAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ["id", "consultant", "start_time", "end_time", "sold_to", "price"]
    list_filter = ('consultant',)
    search_fields = ["id", ]
    advanced_filter_fields = [
        "created"
    ]


@admin.register(SoldTimeSlotSalePaymentInfo)
class SoldTimeSlotSalePaymentInfoAdmin(admin.ModelAdmin):
    change_list_template = 'admin/store/sold_time_slot_sale_payment_info.html'
    date_hierarchy = 'created'
    list_filter = ('consultant',)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['data'] = []

        for obj in qs:
            data = {}
            data["ID"] = obj.id
            data["consultant"] = obj.consultant
            data["time_slot_price"] = obj.price
            data["start_time"] = obj.start_time
            data["end_time"] = obj.end_time
            data["created"] = obj.created
            data["orders"] = list(obj.order_set.all().values_list('id', flat=True))
            data["orders_total"] = list(obj.order_set.all().values_list('total', flat=True))
            data["orders_subtotal"] = list(obj.order_set.all().values_list('subtotal', flat=True))
            response.context_data['data'].append(data)

        return response

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(SoldTimeSlotSale, SoldTimeSlotSaleAdmin)
