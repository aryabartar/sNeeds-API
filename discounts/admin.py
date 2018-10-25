from django.contrib import admin
from .models import CafeImage , Cafe,Discount, UserDiscount

# Register your models here.
class PropertyImageInline(admin.TabularInline):
    model = CafeImage
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ PropertyImageInline, ]

admin.site.register(Cafe, PropertyAdmin)
admin.site.register(Discount)
admin.site.register(UserDiscount)