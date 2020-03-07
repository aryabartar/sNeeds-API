from django.urls import path

from . import views

app_name = "store-package"

urlpatterns = [
    path('store-package-phase-through-detail/<int:id>',
         views.StorePackagePhaseThroughDetailAPIView.as_view(), name="store-package-phase-through-detail"),
    path('store-package-phase-through-list/',
         views.StorePackagePhaseThroughListAPIView.as_view(), name="store-package-phase-through-list"),

    path('store-package-detail/<int:id>',
         views.StorePackageDetailAPIView.as_view(), name="store-package-detail"),
    path('store-package-list/',
         views.StorePackagePhaseThroughListAPIView.as_view(), name="store-package-list"),
]
