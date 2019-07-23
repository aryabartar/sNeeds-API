from django.contrib import admin

from .models import Comment, AdminComment

admin.site.register(Comment)
admin.site.register(AdminComment)