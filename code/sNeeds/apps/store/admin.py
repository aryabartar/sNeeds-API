from django.contrib import admin
from .models import TimeSlotSale, SoldTimeSlotSale, Product

admin.site.register(Product)
admin.site.register(TimeSlotSale)
admin.site.register(SoldTimeSlotSale)


