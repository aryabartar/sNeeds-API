from django.urls import path

from . import views

app_name = "store-package"

urlpatterns = [
    path('marketplace-detail/<int:id>/', views.MarketplaceDetailAPIView.as_view(), name="marketplace-detail"),
    path('marketplace-list/', views.MarketplaceListAPIView.as_view(), name="marketplace-list"),

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

    path('sold-store-package-detail/<int:id>/',
         views.SoldStorePackageDetailAPIView.as_view(), name="sold-store-package-detail"),
    path('sold-store-package-list/',
         views.SoldStorePackageListAPIView.as_view(), name="sold-store-package-list"),

    path('sold-store-unpaid-package-phase-detail/<int:id>/',
         views.SoldStoreUnpaidPackagePhaseDetailAPIView.as_view(), name="sold-store-unpaid-package-phase-detail"),
    path('sold-store-unpaid-package-phase-list/',
         views.SoldStoreUnpaidPackagePhaseListAPIView.as_view(), name="sold-store-unpaid-package-phase-list"),

    path('sold-store-paid-package-phase-detail/<int:id>/',
         views.SoldStorePaidPackagePhaseDetailAPIView.as_view(), name="sold-store-paid-package-phase-detail"),
    path('sold-store-paid-package-phase-list/',
         views.SoldStorePaidPackagePhaseListAPIView.as_view(), name="sold-store-paid-package-phase-list"),

    path('sold-store-package-phase-detail-detail/<int:id>/',
         views.SoldStorePackagePhaseDetailDetailAPIView.as_view(), name="sold-store-package-phase-detail-detail"),
    path('sold-store-package-phase-detail-list/',
         views.SoldStorePackagePhaseDetailListAPIView.as_view(), name="sold-store-package-phase-detail-list"),
]
