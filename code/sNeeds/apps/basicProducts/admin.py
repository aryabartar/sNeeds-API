from django.contrib import admin
from .models import BasicProduct, SoldBasicProduct, DownloadLink, ClassProduct, WebinarProduct, RoomLink
from sNeeds.apps.comments.models import BasicProductRate


class DownloadLinkInline(admin.TabularInline):
    model = DownloadLink
    extra = 1


class RoomLinkInline(admin.TabularInline):
    model = RoomLink
    extra = 1


# class RateFieldInline(admin.TabularInline):
#     model = BasicProductRate
#     extra = 1


class ClassWebinarAdmin(admin.ModelAdmin):
    inlines = (DownloadLinkInline, RoomLinkInline)


class WebinarAdmin(ClassWebinarAdmin):
    pass


class ClassAdmin(ClassWebinarAdmin):
    pass


admin.site.register(ClassProduct, ClassAdmin)
admin.site.register(WebinarProduct, WebinarAdmin)
admin.site.register(BasicProduct)
admin.site.register(SoldBasicProduct)
