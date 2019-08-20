from django.contrib import admin
from .models import TicketMessage, Ticket


@admin.register(TicketMessage)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'title', 'created')


@admin.register(Ticket)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'consultant', 'created')
