from django.contrib import admin

from .models import (
    StorePackage, StorePackagePhase, SoldStorePackage, StorePackagePhaseThrough,
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase, SoldStorePackagePhaseDetail)


class StorePackagePhaseThroughInline(admin.TabularInline):
    model = StorePackagePhaseThrough
    extra = 1


@admin.register(StorePackage)
class StorePackageAdmin(admin.ModelAdmin):
    inlines = (StorePackagePhaseThroughInline,)
    readonly_fields = ["price", "total_price", ]
    list_display = ["id", "title", "total_price"]


@admin.register(SoldStorePackage)
class StorePackageAdmin(admin.ModelAdmin):
    readonly_fields = ["paid_price", "total_price", ]
    list_display = ['id', 'title', 'sold_to', 'consultant']


@admin.register(SoldStoreUnpaidPackagePhase)
class SoldStorePackagePhaseAdmin(admin.ModelAdmin):
    readonly_fields = ['status', 'active', 'sold_store_package',]
    list_display = ['id', 'title', 'price', 'sold_store_package',]


@admin.register(SoldStorePaidPackagePhase)
class SoldStorePackagePhaseAdmin(admin.ModelAdmin):
    exclude = ['sold_to', ]
    readonly_fields = ['status', 'sold_store_package', ]
    list_display = ['id', 'title', 'price', 'sold_store_package',]


admin.site.register(StorePackagePhase)
admin.site.register(SoldStorePackagePhaseDetail)
