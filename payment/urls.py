from django.urls import path, include

from . import views

urlpatterns = [
    path('cart/', views.CartHome.as_view(), name='request'),
    path('verify/', views.verify, name='verify'),
]
