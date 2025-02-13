from django.db.models.signals import post_save
from django.shortcuts import render,redirect
from django.contrib import auth
from django.dispatch import receiver
from users.entity.models import UserDetail
from django.contrib.auth.models import User


def login(request):
    return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')


@receiver(post_save, sender=User)
def create_or_update_user_detail(sender, instance, **kwargs):
    if hasattr(instance, "socialaccount_set") and instance.socialaccount_set.exists():
        social_account = instance.socialaccount_set.first()  # 첫 번째 소셜 계정 가져오기
        user_detail, _ = UserDetail.objects.get_or_create(user=instance) # tuple 반환
        if social_account and social_account.extra_data:
            data = social_account.extra_data  # JSON 데이터
            if user_detail.nickname is None:
                user_detail.nickname = 'qweqwe'
            if social_account.provider == 'naver':
                user_detail_naver(user_detail,data)
            elif social_account.provider == 'kakao':
                user_detail_kakao(user_detail,data)

def user_detail_naver(user_detail, data):
    user_detail.uid = data.get("id")
    user_detail.gender = data.get("gender")
    user_detail.age_range = data.get("age")
    user_detail.extra_data = data  # 원본 JSON 저장
    user_detail.save()

def user_detail_kakao( user_detail ,data ):
    user_detail.uid  = data.get("id")
    gender = data.get("gender")
    if gender == "male":
        user_detail.gender = "M"
    elif gender=="female":
        user_detail.gender = "F"
    user_detail.gender=gender
    user_detail.age_range = data.get("age_range")
    user_detail.extra_data = data  # 원본 JSON 저장
    user_detail.save()