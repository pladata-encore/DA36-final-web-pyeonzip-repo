from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
from django import forms
import re


# Create your models here.
class UserDetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    uid= models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age_range = models.CharField(max_length=10, blank=True, null=True)
    reward=models.IntegerField(blank=True, null=False, default=0)
    profile=models.ImageField(upload_to='profile/',null=True, blank=True, default='profile/default.jpg',max_length=500)
    email=models.EmailField(blank=True, null=False, default='')

    def save(self, *args, **kwargs):
        if not self.pk and not self.nickname:  # 처음 생성될 때만 자동 생성
            base_nickname = slugify(self.user.username)  # 기본적으로 username 기반 생성
            nickname = base_nickname
            count = 1
            while UserDetail.objects.filter(nickname=nickname).exists():
                nickname = f"{base_nickname}{count}"
                count += 1
            self.nickname = nickname

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nickname


class MypageUpdateForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['uid','nickname','profile']

        labels = {
            'uid' : ' 유저 아이디',
            'nickname': '유저 닉네임',
            'profile': '유저 프로필'
        }
        widgets = {
            'profile' : forms.ClearableFileInput(attrs={'class':'hidden-file-input'}),
            'nickname': forms.TextInput(attrs={'class':'form-control','placeholder':'변경할 닉네임을 작성해주세요'}),
        }
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname').strip()

        if not re.match('^[A-Za-z0-9_]+$',nickname):
            raise forms.ValidationError("닉네임은 영어 대소문자, 숫자, _만 사용 가능합니다.")

        if len(nickname) < 8 or len(nickname) > 20:
            raise forms.ValidationError("닉네임은 8자 이상, 30자 미만이어야 합나디.")

        if UserDetail.objects.filter(nickname=nickname).exclude(uid=self.instance.uid).exists():
            raise forms.ValidationError("이미 사용중인 닉네임 입니다.")

        return nickname
