from django.urls import path
from . import views
app_name = "store"

urlpatterns = [
    path('time-slot-sales/', views.TimeSlotSailList.as_view(), name="time-slot-sale-list"),
    path('time-slot-sales/<int:id>/', views.TimeSlotSaleDetail.as_view(), name="time-slot-sale-detail"),
    path('sold-time-slot-sales/', views.SoldTimeSlotSailList.as_view(), name="time-slot-sale-list"),
    # path('sold-time-slot-sales/<int:id>/', views.SoldTimeSlotSaleDetail.as_view(), name="time-slot-sale-detail"),
]
