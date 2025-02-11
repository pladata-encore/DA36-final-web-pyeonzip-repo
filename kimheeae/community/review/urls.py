from board.controller import board_views
from review import views

app_name = 'review'
from django.urls import path

urlpatterns = [
    path('review_write/', views.review_write, name='review_write'),
]

