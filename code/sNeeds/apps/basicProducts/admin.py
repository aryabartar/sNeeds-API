from django.contrib import admin
from .models import BasicProduct, SoldBasicProduct, DownloadLink, ClassProduct, WebinarProduct, RoomLink, \
    SoldClassProduct, SoldWebinarProduct, WebinarRoomLink, ClassRoomLink, ClassWebinar


class DownloadLinkInline(admin.TabularInline):
    model = DownloadLink
    extra = 1


class RoomLinkInline(admin.TabularInline):
    model = RoomLink
    extra = 1


class ClassWebinarAdmin(admin.ModelAdmin):
    inlines = (DownloadLinkInline,)


class WebinarAdmin(ClassWebinarAdmin):
    pass


class ClassAdmin(ClassWebinarAdmin):
    pass


admin.site.register(ClassProduct, ClassAdmin)
admin.site.register(WebinarProduct, WebinarAdmin)
admin.site.register(SoldClassProduct)
admin.site.register(SoldWebinarProduct)
admin.site.register(ClassWebinar)
admin.site.register(ClassRoomLink)
admin.site.register(WebinarRoomLink)
