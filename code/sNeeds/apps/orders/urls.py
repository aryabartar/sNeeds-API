from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name="order-list"),
    path('orders/<int:id>/', views.OrderDetailView.as_view(), name="order-detail"),
]
