from django.contrib import admin

from .models import (StorePackage, StorePackagePhase, SoldStorePackage, StorePackagePhaseThrough)


class StorePackageDetailPhaseThroughInline(admin.TabularInline):
    model = StorePackagePhaseThrough
    extra = 1


class StorePackageDetailAdmin(admin.ModelAdmin):
    inlines = (StorePackageDetailPhaseThroughInline,)


# admin.site.register(SoldStorePackage)
admin.site.register(StorePackagePhase)
admin.site.register(StorePackage, StorePackageDetailAdmin)
