from django.urls import path
from sNeeds.apps.basicProducts import views
app_name = "basic-product"

urlpatterns = [
    path('basic-products/', views.BasicProductList.as_view(), name="basic-product-list"),
    path('basic-products/<slug:slug>/', views.BasicProductDetail.as_view(), name="basic-product-detail"),

    path('class-products/', views.ClassProductList.as_view(), name="class-product-list"),
    path('class-products/<slug:slug>/', views.ClassProductDetail.as_view(), name="class-product-detail"),

    path('webinar-products/', views.WebinarProductList.as_view(), name="webinar-product-list"),
    path('webinar-products/<slug:slug>/', views.WebinarProductDetail.as_view(), name="webinar-product-detail"),

    path('sold-basic-products/', views.SoldBasicProductList.as_view(), name="sold-basic-product-list"),
    path('sold-basic-products/<int:id>/', views.SoldBasicProductDetail.as_view(), name="sold-basic-product-detail"),

    path('sold-class-products/', views.SoldClassProductList.as_view(), name="sold-class-product-list"),
    path('sold-class-products/<int:id>/', views.SoldClassProductDetail.as_view(), name="sold-class-product-detail"),

    path('sold-webinar-products/', views.SoldWebinarProductList.as_view(), name="sold-webinar-product-list"),
    path('sold-webinar-products/<int:id>/', views.SoldWebinarProductDetail.as_view(), name="sold-webinar-product-detail"),

    path('class-room-links/', views.ClassRoomLinkList.as_view(), name="class-room-link-list"),
    path('class-room-links/<int:id>/', views.ClassRoomLinkDetail.as_view(), name="class-room-link-detail"),

    path('webinar-room-links/', views.WebinarRoomLinkList.as_view(), name="webinar-room-link-list"),
    path('webinar-room-links/<int:id>/', views.WebinarRoomLinkDetail.as_view(), name="webinar-room-link-detail"),

]
