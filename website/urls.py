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

app_name = "website"
urlpatterns = [
                  path('', views.home, name="home"),
                  path('posts/<str:slug>', views.get_post, name="posts"),
                  path('tmp/', views.tmp, name="tmp"),
                  path('booklets/', views.booklet_home, name="booklets_home"),
                  path('booklets/search/', include('haystack.urls') , name="booklets_search"),
                  path('booklets/user-upload', views.upload_booklet, name="upload_booklet"),
                  path('booklets/<str:slug>', views.BookletFieldView.as_view(), name="booklets_field"),
                  path('booklets/download/new/<str:slug>', views.get_booklet, name="booklets"),
                  path('booklets/<str:field_slug>/<str:slug>', views.BookletTopicView.as_view(), name="booklets_topic"),
                  re_path(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
                  path('blog/', views.blog_posts),#Automatically goes to first page (default page is 1)
                  path('blog/<int:page>', views.blog_posts, name="blog"),#Goes to specific page of the blog
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
