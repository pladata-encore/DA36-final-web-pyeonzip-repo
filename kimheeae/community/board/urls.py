
app_name = 'board'

from django.urls import path

from board.controller import board_views

urlpatterns = [
    path('community_main/', board_views.community_main, name="community_main"),
    path('board_list/', board_views.board_list, name="board_list"),
    path('board_write/', board_views.board_write, name='board_write'),

]
