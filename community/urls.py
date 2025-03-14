"""
URL configuration for pyeonzip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView
from community.controller import community_views

app_name='community'
urlpatterns = [
    path("community_list/", community_views.community_list, name="community_list"),
    path("community_write/", community_views.community_write, name="community_write"),
    path("community_save/", community_views.community_save, name="community_save"),
    path("vote_community/", community_views.vote_community, name="vote_community"),
    path("community_detail/<int:communityId>/", community_views.community_detail, name="community_detail"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
