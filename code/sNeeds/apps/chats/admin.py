from django.contrib import admin

from . import models

admin.site.register(models.Chat)
admin.site.register(models.Message)
admin.site.register(models.TextMessage)
admin.site.register(models.FileMessage)
admin.site.register(models.VoiceMessage)
admin.site.register(models.ImageMessage)
