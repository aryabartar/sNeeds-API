from django.urls import path

from . import views

app_name = "store-package"

urlpatterns = [
    path('store-package-detail/<str:slug>/',
         views.StorePackageDetailAPIView.as_view(), name="store-package-detail"),
    path('store-package-list/',
         views.StorePackageListAPIView.as_view(), name="store-package-list"),

    path('store-package-phase-through-detail/<int:id>/',
         views.StorePackagePhaseThroughDetailAPIView.as_view(), name="store-package-phase-through-detail"),
    path('store-package-phase-through-list/',
         views.StorePackagePhaseThroughListAPIView.as_view(), name="store-package-phase-through-list"),

    path(
        'consultant-sold-store-package-accept-request-detail/<int:id>/',
        views.ConsultantSoldStorePackageAcceptRequestDetailAPIView.as_view(),
        name="consultant-sold-store-package-accept-request-detail"
    ),
    path(
        'consultant-sold-store-package-accept-request-list/',
        views.ConsultantSoldStorePackageAcceptRequestListAPIView.as_view(),
        name="consultant-sold-store-package-accept-request-list"
    ),

]
