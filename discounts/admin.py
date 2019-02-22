from django.contrib import admin
from .models import CafeImage, Cafe, Discount, UserDiscount, CafeProfile, UserDiscountArchive


# Register your models here.
class PropertyImageInline(admin.TabularInline):
    model = CafeImage
    extra = 3


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, ]


admin.site.register(Cafe, PropertyAdmin)
admin.site.register(Discount)
admin.site.register(UserDiscount)
admin.site.register(CafeProfile)
admin.site.register(UserDiscountArchive)
admin.site.register(CafeImage)
