from django.contrib import admin
from .models import BasicProduct, SoldBasicProduct, DownloadLink, ClassProduct, WebinarProduct, RoomLink, \
    SoldClassProduct, SoldWebinarProduct, WebinarRoomLink, ClassRoomLink, ClassWebinar, HoldingDateTime, Lecturer, \
    QuestionAnswer, SoldClassWebinar


class DownloadLinkInline(admin.TabularInline):
    model = DownloadLink
    extra = 1


class HoldingDateTimeInline(admin.TabularInline):
    model = HoldingDateTime
    extra = 1


class LecturerInline(admin.TabularInline):
    model = Lecturer
    extra = 1


class QuestionAnswerInline(admin.StackedInline):
    model = QuestionAnswer
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
# admin.site.register(SoldClassWebinar)
# admin.site.register(ClassWebinar)
admin.site.register(ClassRoomLink)
admin.site.register(WebinarRoomLink)
admin.site.register(HoldingDateTime)
admin.site.register(QuestionAnswer)
admin.site.register(Lecturer)
