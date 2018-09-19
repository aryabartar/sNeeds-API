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
from django.urls import path, include
from . import views

app_name = "website"
urlpatterns = [
                  path('', views.home, name="home"),
                  path('posts/<str:slug>', views.get_post, name="posts"),
                  path('booklets/<int:pk>', views.get_booklet, name="booklets"),
                  path('categories/<str:hierarchy>', views.show_category, name="categories"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
