from django.urls import path
from . import views

urlpatterns = [
    path('TimeSlotSales/', views.TimeSlotSailList.as_view(), name="time-slot-list"),

]
