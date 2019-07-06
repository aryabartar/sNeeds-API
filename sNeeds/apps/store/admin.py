from django.contrib import admin
from . import models


class TimeSlotSaleAdmin(admin.ModelAdmin):
    list_display = ('get_buyer_username', 'get_consultant_username',)


# Register your models here.
admin.site.register(models.TimeSlotSale, TimeSlotSaleAdmin)
