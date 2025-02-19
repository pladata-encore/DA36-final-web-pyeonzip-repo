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
from product.controller import views, select_product_views
from product.controller.select_product_views import select_product_list

app_name='product'
urlpatterns = [
    path("select_product",select_product_views.select_product_list,name="select_product"),
    # path("", views.index, name="index"),
    path("all_product_pagination",views.all_product_pagination,name="all_product_pagination"),
    path("latest_product_pagination",views.latest_product_pagination,name="latest_product_pagination"),
    path("product_detail/<int:product_id>/",views.product_detail,name="product_detail"),
    path("product_likes/<int:product_id>/",views.product_likes,name="product_likes"),
    path("latest", views.latest_product_showcase,name="latest_product_showcase"),
]