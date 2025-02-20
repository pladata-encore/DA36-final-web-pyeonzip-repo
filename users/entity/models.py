from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# from allauth.socialaccount.models import SocialAccount
from django import forms
# from allauth.socialaccount.signals import pre_social_login
import re


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


class MypageUpdateForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['uid','nickname', 'profile']

        labels = {
            'uid' : ' 유저 아이디',
            'nickname': '유저 닉네임',
            'profile': '유저 프로필'
        }
        widgets = {
            'nickname': forms.TextInput(attrs={'class':'form-control','placeholder':'변경할 닉네임을 작성해주세요'}),
        }
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname').strip()

        if not re.match('^[A-Za-z0-9]+$',nickname):
            raise forms.ValidationError("닉네임은 영어 대소문자, 숫자, _만 사용 가능합니다.")

        if len(nickname) < 8 or len(nickname) > 20:
            raise forms.ValidationError("닉네임은 8자 이상, 30자 미만이어야 합나디.")

        if UserDetail.objects.filter(nickname=nickname).exclude(uid=self.instance.uid).exists():
            raise forms.ValidationError("이미 사용중인 닉네임 입니다.")

        return nickname
