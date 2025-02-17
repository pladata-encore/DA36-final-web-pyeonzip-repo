# Create your models here.
import os

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL
from product.entity.models import Product

class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)  # okay
    authorId = models.ForeignKey(User, null=True, blank=True,related_name='User_reviews',on_delete=SET_NULL)  # author_id, user_id [erd_cloud 통일]
    productId = models.ForeignKey(Product, null=True, blank=True, related_name='Product_reviews',on_delete=SET_NULL)
    tasteContent = models.TextField()
    priceContent = models.TextField()
    convenienceContent = models.TextField()  # erd cloud 추가
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    reviewImageUrl = models.ImageField(upload_to='review/', null=True, blank=True)  # url, imageField, null, blank true
    recommender = models.ManyToManyField(User, null=True, blank=True,related_name='Review_recommender',through='ReviewRecommender')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어

class ReviewRecommender(models.Model):
    recommenderId = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    reviewId = models.ForeignKey(Review, null=True, blank=True,on_delete=SET_NULL)
    recommended_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_recommender'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['productId', 'tasteContent', 'priceContent', 'convenienceContent',
                  'reviewImageUrl']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'tasteContent': '맛 리뷰',
            'priceContent': '가격 리뷰',
            'convenienceContent': '편리성 리뷰',
            'productId': '제품',
            'reviewImageUrl': '제품 사진',
        }
