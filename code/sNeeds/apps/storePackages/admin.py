# from django.contrib import admin
#
# from .models import (
#     StorePackage, StorePackagePhase, SoldStorePackage, StorePackagePhaseThrough, SoldStorePackagePhase
# )
#
#
# class StorePackagePhaseThroughInline(admin.TabularInline):
#     model = StorePackagePhaseThrough
#     extra = 1
#
#
# @admin.register(StorePackage)
# class StorePackageAdmin(admin.ModelAdmin):
#     inlines = (StorePackagePhaseThroughInline,)
#     readonly_fields = ["price", "total_price", ]
#
#
# @admin.register(SoldStorePackage)
# class StorePackageAdmin(admin.ModelAdmin):
#     readonly_fields = ["price", "total_price", ]
#     list_display = ['id', 'title', 'sold_to', 'consultant']
#
#
# @admin.register(SoldStorePackagePhase)
# class SoldStorePackagePhaseAdmin(admin.ModelAdmin):
#     # readonly_fields = ["price", "total_price", ]
#     # list_display = ['id', 'title', 'sold_to', 'consultant']
#     pass
#
# admin.site.register(StorePackagePhase)
