from django.db.models.signals import post_save
from django.shortcuts import render,redirect
from django.contrib import auth,messages
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from users.models import UserDetail,UserDetailForm
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

def login(request):
    return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')



# @receiver(post_save, sender=User)
# def create_or_update_user_detail(sender, instance, created, **kwargs):
#     if hasattr(instance, "socialaccount_set"):
#         social_account = instance.socialaccount_set.first()  # 첫 번째 소셜 계정 가져오기
#         if social_account and social_account.extra_data:
#             data = social_account.extra_data  # JSON 데이터=
#             gender = data.get("gender")
#
#             user_detail, _ = UserDetail.objects.get_or_create(user=instance)
#
#             user_detail.gender = gender
#             user_detail.extra_data = data  # 원본 JSON 저장
#             user_detail.save()


def user_detail_naver(instance, data):
    print("instance",instance)
    print("data",data)
    uid = data.get("id")
    print(uid)
    gender = data.get("gender")
    print(gender)
    birthday = data.get("birthday")
    print(birthday)
    user_detail, _ = UserDetail.objects.get_or_create(user=instance) # tuple 반환
    print("1",user_detail)
    user_detail.uid = uid
    user_detail.gender = gender
    # user_detail.birthday = birthday
    print("2",user_detail)
    user_detail.extra_data = data  # 원본 JSON 저장
    user_detail.save()

def user_detail_kakao( instance ,data ):
    uid = data.get("uuid")
    gender = data.get("gender")
    if gender == "male":
        gender = "M"
    else:
        gender = "F"
    birthday = data.get("birthday")

    user_detail = UserDetail.objects.get_or_create(user=instance)
    user_detail.uid = uid
    user_detail.gender = gender
    user_detail.birthday = birthday
    user_detail.extra_data = data  # 원본 JSON 저장
    user_detail.save()