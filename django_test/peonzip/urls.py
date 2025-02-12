
from peonzip import views
from django.urls import path

# app_name+index 가 url 로 사용되는 것임 ! (index.html에서)
app_name='qna'
urlpatterns = [
    # 기본 view
    path("", views.index, name="index"),
]