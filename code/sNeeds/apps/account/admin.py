from django.contrib import admin

from . import models

admin.site.register(models.University)
admin.site.register(models.FieldOfStudy)
admin.site.register(models.Country)
admin.site.register(models.StudentDetailedInfo)
admin.site.register(models.StudentFormApplySemesterYear)


@admin.register(models.StudentFormFieldsChoice)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'id')
    list_filter = ('category', )
