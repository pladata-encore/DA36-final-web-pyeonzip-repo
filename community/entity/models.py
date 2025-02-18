from datetime import timedelta
from django.utils.timezone import now

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL
from product.entity.models import Product


class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=10)


class Community(models.Model):
    communityId = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, null=True, blank=True,on_delete=SET_NULL)
    author = models.ForeignKey(User, null=True, blank=True, related_name='User_community',on_delete=SET_NULL)
    products = models.ManyToManyField(Product, blank=True, related_name='Community_products') # product 여러개 지정 가능하도록 ManyToManyField로 변경
    communityTitle = models.CharField(max_length=50)
    communityContent = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True,default=None)
    voter = models.ManyToManyField(User, null=True, blank=True, related_name='Community_voters',through='CommunityVoters')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어

    def save(self, *args, **kwargs):
        if not self.deadline:
            self.deadline = now().date() + timedelta(days=30)
        super().save(*args, **kwargs)

class CommunityVoters(models.Model):
    voterId = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    communityId = models.ForeignKey(Community, null=True, blank=True,on_delete=SET_NULL)
    voted_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_voters'

class CommunityForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        required=False
    )
    class Meta:
        model = Community
        fields = ['category', 'communityTitle', 'communityContent', 'products']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'category': '카테고리',
            'communityTitle': '제목',
            'communityContent': '내용',
            'products': '제품 선택',
        }




