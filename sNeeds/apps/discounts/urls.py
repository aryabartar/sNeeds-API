from django.urls import path

from . import views

app_name = "discount"

urlpatterns = [
    path('cart-consultant-discount/', views.CartConsultantDiscountListView.as_view()),
]
