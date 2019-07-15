from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path('carts/', views.CartList.as_view()),
]
