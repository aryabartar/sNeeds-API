from django.urls import path, include

from . import views

urlpatterns = [
    path('cart/', views.CartHome.as_view(), name='cart'),
    path('cart/update/', views.CartUpdate.as_view()),
    path('verify/', views.verify, name='verify'),
]
