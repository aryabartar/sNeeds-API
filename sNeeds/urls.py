"""sNeeds URL Configuration

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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('docs/', include('sNeeds.apps.docs.urls')),

                  path('auth/', include('sNeeds.apps.customAuth.urls')),
                  path('account/', include('sNeeds.apps.account.urls')),
                  path('store/', include('sNeeds.apps.store.urls')),
                  path('cart/', include('sNeeds.apps.carts.urls')),
                  path('order/', include('sNeeds.apps.orders.urls')),
                  path('payment/', include('sNeeds.apps.payments.urls')),
                  path('comment/', include('sNeeds.apps.comments.urls')),
                  path('user-file/', include('sNeeds.apps.userfiles.urls')),
                  path('discount/', include('sNeeds.apps.discounts.urls')),
                  path('videochats/', include('sNeeds.apps.videochats.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
