from django.contrib import admin

from django.contrib import admin

from .models import Notification, EmailNotification


@admin.register(EmailNotification)
class DiscountAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'sent',]
