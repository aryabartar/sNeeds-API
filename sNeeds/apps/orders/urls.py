from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path('orders/', views.OrderListView.as_view()),
]
