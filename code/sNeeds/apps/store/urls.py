from django.urls import path
from . import views
app_name = "store"

urlpatterns = [
    path('time-slot-sales/', views.TimeSlotSailList.as_view(), name="time-slot-sale-list"),
    path('time-slot-sales/<int:id>/', views.TimeSlotSaleDetail.as_view(), name="time-slot-sale-detail"),
    path('sold-time-slot-sales/', views.SoldTimeSlotSaleList.as_view(), name="sold-time-slot-sale-list"),
    path('sold-time-slot-sales/<int:id>/', views.SoldTimeSlotSaleDetail.as_view(), name="sold-time-slot-sale-detail"),
]
