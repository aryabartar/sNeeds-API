from django.contrib import admin

from .models import Order, SoldOrder

admin.site.register(Order)
admin.site.register(SoldOrder)
