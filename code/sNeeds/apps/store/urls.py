from django.urls import path
from . import views
app_name = "store"

urlpatterns = [
    path('time-slot-sales/', views.TimeSlotSaleListAPIView.as_view(), name="time-slot-sale-list"),
    path('time-slot-sales/<int:id>/', views.TimeSlotSaleDetailAPIView.as_view(), name="time-slot-sale-detail"),
    path('sold-time-slot-sales/', views.SoldTimeSlotSaleListAPIView.as_view(), name="sold-time-slot-sale-list"),
    path('sold-time-slot-sales/<int:id>/', views.SoldTimeSlotSaleDetailAPIView.as_view(), name="sold-time-slot-sale-detail"),
    path('sold-time-slot-sales-safe/', views.SoldTimeSlotSaleSafeListAPIView.as_view(), name="sold-time-slot-sale-safe-list"),
    path('sold-time-slot-sales-safe/<int:id>/', views.SoldTimeSlotSaleSafeDetailAPIView.as_view(), name="sold-time-slot-sale-safe-detail"),
]
