from django.contrib import admin

import sNeeds.apps.customAuth.models
from . import models

# Register your models here.
admin.site.register(sNeeds.apps.customAuth.models.ConsultantProfile)
admin.site.register(models.University)
admin.site.register(models.FieldOfStudy)
admin.site.register(models.Country)