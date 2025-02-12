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
    categoryId = models.ForeignKey(Category, null=True, blank=True,on_delete=SET_NULL)
    authorId = models.ForeignKey(User, null=True, blank=True, related_name='User_community',on_delete=SET_NULL)
    productId = models.ForeignKey(Product, null=True, blank=True, related_name='Product_community',on_delete=SET_NULL)  # 3개가 참조 가능 ? ? ?  ? ?
    communityTitle = models.CharField(max_length=100)
    communityContent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    voter = models.ManyToManyField(User, null=True, blank=True, related_name='Community_voters',through='CommunityVoters')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어


class CommunityVoters(models.Model):
    voterId = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    communityId = models.ForeignKey(Community, null=True, blank=True,on_delete=SET_NULL)
    voted_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_voters'

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['categoryId', 'communityTitle', 'communityContent', 'productId']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'categoryId': '카테고리',
            'communityTitle': '제목',
            'communityContent': '내용',
            'productId': '제품 선택',
        }




