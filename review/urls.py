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
import os

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView
from review.controller import review_views
app_name='review'
urlpatterns = [
    path('review_write/', review_views.review_write, name='review_write'),
    path('review_recommend/<int:review_id>', review_views.review_recommend, name='review_recommend'),
    path('analyze_review/', review_views.analyze_review_sentiment, name='analyze_review_sentiment'),
    path('analyze_review_keyword/', review_views.analyze_review_keyword, name='analyze_review_keyword'),
]
