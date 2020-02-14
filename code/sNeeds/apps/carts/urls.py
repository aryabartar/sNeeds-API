from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path('carts/', views.CartListView.as_view(), name="cart-list"),
    path('carts/<int:id>/', views.CartDetailView.as_view(), name="cart-detail"),
]
