from django.contrib import admin

from . import models

admin.site.register(models.Chat)
admin.site.register(models.Message)
admin.site.register(models.File)
admin.site.register(models.Voice)
admin.site.register(models.Image)
