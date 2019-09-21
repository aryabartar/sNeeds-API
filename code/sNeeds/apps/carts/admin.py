from django.contrib import admin

from .models import Cart, SoldCart

admin.site.register(Cart)
admin.site.register(SoldCart)
