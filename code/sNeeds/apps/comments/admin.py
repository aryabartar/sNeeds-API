from django.contrib import admin

from .models import ConsultantComment, ConsultantAdminComment, SoldTimeSlotRate, BasicProductRateField, \
    BasicProductRate, SoldBasicProductRateFieldThrough, SoldBasicProductRate

admin.site.register(ConsultantComment)
admin.site.register(ConsultantAdminComment)


@admin.register(SoldTimeSlotRate)
class SoldTimeSlotRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'rate', 'sold_time_slot',)


class BasicProductRateFieldInline(admin.TabularInline):
    model = BasicProductRateField
    extra = 1


@admin.register(BasicProductRate)
class BasicProductRateAdmin(admin.ModelAdmin):
    inlines = (BasicProductRateFieldInline,)


class SoldBasicProductRateFieldThroughInline(admin.TabularInline):
    model = SoldBasicProductRateFieldThrough
    extra = 1


@admin.register(SoldBasicProductRate)
class SoldBasicProductRateAdmin(admin.ModelAdmin):
    inlines = (SoldBasicProductRateFieldThroughInline,)
