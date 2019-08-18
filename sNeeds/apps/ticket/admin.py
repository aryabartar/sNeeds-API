from django.contrib import admin
from .models import TicketMessage, Ticket


def text_shorter(obj):
    text_splited = obj.text.split(' ')
    text = ' '.join(text_splited[:5])
    text += "..."
    return text
text_shorter.short_description = 'text'


def title_shorter_for_ticket_message(obj):
    title_splited = obj.ticket.title.split(' ')
    title = ' '.join(title_splited[:5])
    title += "..."
    return title
title_shorter_for_ticket_message.short_description = 'title'


@admin.register(TicketMessage)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', text_shorter, title_shorter_for_ticket_message, 'created')\


def title_shorter_for_ticket(obj):
    title_splited = obj.title.split(' ')
    title = ' '.join(title_splited[:5])
    title += "..."
    return title
title_shorter_for_ticket.short_description = 'title'


@admin.register(Ticket)
class ConsultantDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', title_shorter_for_ticket, 'user', 'consultant', 'created')
