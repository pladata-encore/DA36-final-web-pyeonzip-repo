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
from users.controller import views, mypage_views, mywrite_views

app_name='users'
urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('mypage/', mypage_views.mypage, name="mypage"),
    path('mypage_update/',mypage_views.mypage_update, name="mypage_update"),

    path('check_duplicate/', mypage_views.check_nickname_duplicate, name="check_nickname_duplicate"),

    path('my_review/', mywrite_views.my_review, name="my_review"),
    path('my_community/', mywrite_views.my_community, name="my_community"),
    path('my_review_recommends/', mywrite_views.my_review_recommends, name="my_review_recommends"),
]