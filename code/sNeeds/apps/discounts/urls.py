from django.urls import path

from . import views

app_name = "discount"

urlpatterns = [
    path('time-slot-sale-number-discounts/', views.TimeSlotSaleNumberDiscountListView.as_view()),
    path('cart-discounts/', views.CartDiscountListView.as_view(), name='cart-discount-list'),
    path('cart-discounts/<int:id>/', views.CartDiscountDetailView.as_view(),
         name="cart-discount-detail"),

    path('consultant-discounts/', views.ConsultantForUserDiscountListCreateAPIView.as_view(),
         name='consultant-discount-list'),

    path('consultant-discounts/<int:id>/', views.ConsultantForUserDiscountRetrieveDestroyAPIView.as_view(),
         name='consultant-discount-detail'),

    path('consultant-interact-users/', views.ConsultantInteractUserListAPIView.as_view(),
         name='consultant-interact-user-list')
]
