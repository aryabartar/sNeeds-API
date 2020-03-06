from django.urls import path

from . import views

app_name = "store-package"

urlpatterns = [
    path('store-package-detail-phase-through/',
         views.StorePackageDetailPhaseThroughDetailAPIView.as_view(), name="store-package-detail-phase-through-detail"),
]
