from django.urls import path
from . import views
app_name = "webinars"

urlpatterns = [
    path('webinars/', views.WebinarList.as_view(), name="webinars-list"),
    path('webinars/<slug:slug>/', views.WebinarDetail.as_view(), name="webinar-detail"),
    path('sold-webinar/', views.SoldWebinarList.as_view(), name="sold-webinars-list"),
    path('sold-webinar/<int:id>/', views.SoldWebinarDetail.as_view(), name="sold-webinar-detail"),
]
