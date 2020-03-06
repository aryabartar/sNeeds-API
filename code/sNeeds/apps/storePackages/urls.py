from django.urls import path

from . import views

app_name = "store-package"

urlpatterns = [
    path('store-package-phase-through/',
         views.StorePackagePhaseThroughDetailAPIView.as_view(), name="store-package-phase-through-detail"),
]
