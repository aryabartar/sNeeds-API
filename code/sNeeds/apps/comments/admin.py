from django.contrib import admin

from .models import Comment, AdminComment, SoldTimeSlotRate

admin.site.register(Comment)
admin.site.register(AdminComment)
admin.site.register(SoldTimeSlotRate)