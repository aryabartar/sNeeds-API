"""Ticket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = "ticket"

urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name="ticket-list"),
    path('tickets/<int:id>/', views.TicketDetailView.as_view(), name="ticket-detail"),
    path('messages/', views.MessageListView.as_view() , name="message-list"),
    path('messages/<int:id>/', views.MessageDetailView.as_view() , name="message-detail"),
]
