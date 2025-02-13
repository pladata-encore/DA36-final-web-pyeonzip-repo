from django import forms
from users.entity.models import UserDetail


class MyPage(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['uid', 'nickname', 'profile']

        labels = {
            'uid': '유저 아이디',
            'nickname': '유저 닉네임',
            'profile': '유저 프로필'
        }
