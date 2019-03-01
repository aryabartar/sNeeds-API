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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from discounts import urls as discounts_urls
from account import urls as account_urls
from blog import urls as blog_urls
from booklet import urls as booklet_urls
from payment import urls as payment_urls
from classes import urls as class_urls

urlpatterns = [
                  path('account/', include(account_urls)),
                  path('admin/', admin.site.urls),
                  path('cafe/', include(discounts_urls)),
                  path('blog/', include(blog_urls)),
                  path('booklet/', include(booklet_urls)),
                  path('payment/', include(payment_urls)),
                  path('class/', include(class_urls)),

                  path('api-auth/', include('rest_framework.urls'))
              ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


