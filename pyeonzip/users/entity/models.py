from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# from allauth.socialaccount.models import SocialAccount
from django import forms
# from allauth.socialaccount.signals import pre_social_login


# Create your models here.
class UserDetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    uid= models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age_range = models.CharField(max_length=10, blank=True, null=True)
    reward=models.IntegerField(blank=True, null=False, default=0)
    profile=models.ImageField(upload_to='profile/',null=True, blank=True)
    email=models.EmailField(blank=True, null=False, default='')


class mypageUpdateForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['uid', 'nickname', 'profile']

        labels = {
            'uid': '유저 아이디',
            'nickname': '유저 닉네임',
            'profile': '유저 프로필'
        }
