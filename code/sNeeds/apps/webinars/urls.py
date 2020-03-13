from django.urls import path
from sNeeds.apps.webinars import views
app_name = "webinars"

urlpatterns = [
    path('webinars/', views.WebinarList.as_view(), name="webinar-list"),
    path('webinars/<slug:slug>/', views.WebinarDetail.as_view(), name="webinar-detail"),
    path('sold-webinars/', views.SoldWebinarList.as_view(), name="sold-webinar-list"),
    path('sold-webinars/<int:id>/', views.SoldWebinarDetail.as_view(), name="sold-webinar-detail"),
]
