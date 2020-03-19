from django.contrib import admin

from .models import (
    StorePackage, StorePackagePhase, SoldStorePackage, StorePackagePhaseThrough, SoldStorePackagePhase
)


class StorePackagePhaseThroughInline(admin.TabularInline):
    model = StorePackagePhaseThrough
    extra = 1


@admin.register(StorePackage)
class StorePackageAdmin(admin.ModelAdmin):
    inlines = (StorePackagePhaseThroughInline,)
    readonly_fields = ["price", "total_price", ]


admin.site.register(StorePackagePhase)
admin.site.register(SoldStorePackage)
admin.site.register(SoldStorePackagePhase)
