from django.contrib import admin

from . import models

admin.site.register(models.University)
admin.site.register(models.FieldOfStudy)
admin.site.register(models.Country)
# admin.site.register(models.StudentDetailedInfo)
# admin.site.register(models.StudentFormFieldsChoice)
# admin.site.register(models.StudentFormApplySemesterYear)
