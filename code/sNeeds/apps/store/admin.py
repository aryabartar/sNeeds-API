from django.contrib import admin
from .models import TimeSlotSale, SoldTimeSlotSale, Product, ConsultantAcceptSoldProductRequest

admin.site.register(Product)
admin.site.register(TimeSlotSale)
admin.site.register(SoldTimeSlotSale)
admin.site.register(ConsultantAcceptSoldProductRequest)
