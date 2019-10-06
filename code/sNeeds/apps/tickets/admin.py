from django.contrib import admin

from .models import Message, Ticket


def get_title(obj):
    return obj.ticket.title
get_title.short_description = 'title'


@admin.register(Message)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', get_title, 'created')


@admin.register(Ticket)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'consultant', 'created')
