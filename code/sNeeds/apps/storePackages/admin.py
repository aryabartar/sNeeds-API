from django.contrib import admin

from .models import (
    StorePackage, StorePackagePhase, SoldStorePackage, StorePackagePhaseThrough,
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase, SoldStorePackagePhaseDetail,
    ConsultantSoldStorePackageAcceptRequest, StorePackagePhaseDetail
)


class StorePackagePhaseThroughInline(admin.TabularInline):
    model = StorePackagePhaseThrough
    extra = 1


@admin.register(StorePackage)
class StorePackageAdmin(admin.ModelAdmin):
    inlines = (StorePackagePhaseThroughInline,)
    readonly_fields = ["price", "total_price", ]
    list_display = ["id", "title", "total_price"]


@admin.register(SoldStorePackage)
class SoldStorePackageAdmin(admin.ModelAdmin):
    readonly_fields = ["paid_price", "total_price", ]
    list_display = ['id', 'title', 'sold_to', 'consultant']


@admin.register(SoldStoreUnpaidPackagePhase)
class SoldStoreUnpaidPackagePhaseAdmin(admin.ModelAdmin):
    readonly_fields = ['status', 'sold_store_package', ]
    list_display = ['id', 'title', 'price', 'sold_store_package', ]


@admin.register(SoldStorePaidPackagePhase)
class SoldStorePaidPackagePhaseAdmin(admin.ModelAdmin):
    exclude = ['sold_to', ]
    readonly_fields = ['status', 'sold_store_package', ]
    list_display = ['id', 'title', 'price', 'sold_store_package', ]


@admin.register(StorePackagePhase)
class StorePackagePhaseAdmin(admin.ModelAdmin):
    filter_horizontal = ['phase_details', ]


admin.site.register(StorePackagePhaseDetail)
admin.site.register(ConsultantSoldStorePackageAcceptRequest)
admin.site.register(SoldStorePackagePhaseDetail)
