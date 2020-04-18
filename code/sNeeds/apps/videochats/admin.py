from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'sold_time_slot', 'created')
    readonly_fields = ["room_id", "user_id", "consultant_id", "user_login_url",
                       "consultant_login_url"]
