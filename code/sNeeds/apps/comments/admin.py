from django.contrib import admin

from .models import ConsultantComment, ConsultantAdminComment, SoldTimeSlotRate

admin.site.register(ConsultantComment)
admin.site.register(ConsultantAdminComment)
admin.site.register(SoldTimeSlotRate)