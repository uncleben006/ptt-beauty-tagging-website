"""ptt_beauty_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from image_tag_app import views as tag_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tag_views.index),
    path('post/<str:slug>/', tag_views.post),
    path('title/<str:slug>/', tag_views.post_title),
    path('data/<str:slug>/', tag_views.data),
    path('img/delete/<str:slug>/<str:img>/', tag_views.delete_img),
    path('tag/delete/<str:slug>/<str:tag>/', tag_views.delete_tag),
    path('title_tag/delete/<str:slug>/<str:tag>/', tag_views.delete_title_tag)
]
