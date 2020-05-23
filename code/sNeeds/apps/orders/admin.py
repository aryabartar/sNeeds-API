from django.contrib import admin

from .models import Order
from advanced_filters.admin import AdminAdvancedFiltersMixin


class OrderAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ["id", "order_id", "user", "total", "subtotal", "created"]
    filter_horizontal = ('sold_products',)
    advanced_filter_fields = (
        "total",
        "created"
    )


admin.site.register(Order, OrderAdmin)
