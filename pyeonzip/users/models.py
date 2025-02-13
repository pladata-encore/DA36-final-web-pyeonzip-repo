from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.socialaccount.models import SocialAccount
from django import forms
from allauth.socialaccount.signals import pre_social_login


# Create your models here.
class UserDetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    uid= models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['nickname', 'birthday']

