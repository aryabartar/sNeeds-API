from django.contrib import admin

from sNeeds.apps.consultants.models import ConsultantProfile, StudyInfo


class StudyInfoInline(admin.TabularInline):
    model = StudyInfo
    extra = 1


@admin.register(ConsultantProfile)
class StorePackageAdmin(admin.ModelAdmin):
    inlines = (StudyInfoInline,)
    readonly_fields = ["rate", ]
    list_display = ["id", "__str__", "user", "rate", "active", ]
