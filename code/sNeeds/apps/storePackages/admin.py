from django.contrib import admin

from .models import (StorePackageDetail, StorePackageDetailPhase, StorePackage, StorePackageDetailPhaseThrough)


class StorePackageDetailPhaseThroughInline(admin.TabularInline):
    model = StorePackageDetailPhaseThrough
    extra = 1


class StorePackageDetailAdmin(admin.ModelAdmin):
    inlines = (StorePackageDetailPhaseThroughInline,)


admin.site.register(StorePackage)
admin.site.register(StorePackageDetailPhase)
admin.site.register(StorePackageDetail, StorePackageDetailAdmin)
