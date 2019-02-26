from django.contrib import admin
from .models import PublicClass, SoldPublicClass

admin.site.register(PublicClass)
admin.site.register(SoldPublicClass)
