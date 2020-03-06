from django.contrib import admin

from .models import (StorePackageDetail, StorePackageDetailPhase, StorePackage, StorePackageDetailPhaseThrough)

# class DepartmentPeopleInline(admin.TabularInline):
#     model = DepartmentPeople
#     extra = 1
#
# class DepartmentAdmin(admin.ModelAdmin):
#     inlines = (DepartmentPeopleInline,)

# admin.site.register(Person, PersonAdmin)
# admin.site.register(Department, DepartmentAdmin)
admin.site.register(StorePackageDetail)
