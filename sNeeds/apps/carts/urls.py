from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path('carts/', views.CartListView.as_view()),
    path('carts/<int:pk>/', views.CartDetailView.as_view()),
]
