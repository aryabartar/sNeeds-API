from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.CartHome.as_view(), name='cart'),
    path('checkout/', views.OrderHome.as_view()),
    path('update/', views.CartUpdate.as_view()),
    path('verify/', views.verify, name='verify'),
]
