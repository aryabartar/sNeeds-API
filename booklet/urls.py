"""sneeds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from . import views

app_name = "booklet"
urlpatterns = [
    path('', views.GetFieldsList.as_view(), name='get_fields_list'),
    path('tags/<str:tag_slug>', views.TagsDetail.as_view(), name='get_fields_list'),
    path('<str:field_slug>/', views.GetField.as_view(), name='get_field'),
    path('<str:field_slug>/<str:topic_slug>/', views.GetTopic.as_view(), name='get_topic'),
    path('<str:field_slug>/<str:topic_slug>/<str:booklet_slug>/', views.GetBooklet.as_view(), name='get_booklet'),
]
