from django.urls import path
from sNeeds.apps.basicProducts import views
app_name = "basic-product"

urlpatterns = [
    path('basic-products/', views.BasicProductList.as_view(), name="basic-product-list"),
    path('basic-products/<slug:slug>/', views.BasicProductDetail.as_view(), name="basic-product-detail"),
    path('sold-basic-products/', views.SoldBasicProductList.as_view(), name="sold-basic-product-list"),
    path('sold-basic-products/<int:id>/', views.SoldBasicProductDetail.as_view(), name="sold-basic-product-detail"),
]
