from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Booklet)
admin.site.register(models.BookletTopic)
admin.site.register(models.BookletField)
admin.site.register(models.Tag)