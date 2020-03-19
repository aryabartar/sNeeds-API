from django.urls import path

from . import views

app_name = "discount"

urlpatterns = [
    path('time-slot-sale-number-discounts/', views.TimeSlotSaleNumberDiscountListView.as_view()),
    path('cart-discounts/', views.CartDiscountListView.as_view(), name='cart-discount-list'),
    path('cart-discounts/<int:id>/', views.CartDiscountDetailView.as_view(),
         name="cart-discount-detail"),
]
