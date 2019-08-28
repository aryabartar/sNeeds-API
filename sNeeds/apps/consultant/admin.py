from django.contrib import admin
from .models import TMPConsultant


@admin.register(TMPConsultant)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'created')