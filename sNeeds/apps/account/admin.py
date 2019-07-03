from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.ConsultantProfile)
admin.site.register(models.University)
admin.site.register(models.FieldOfStudy)