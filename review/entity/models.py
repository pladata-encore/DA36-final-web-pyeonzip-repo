# Create your models here.
import os

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL
from product.entity.models import Product

class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)  # okay
    author = models.ForeignKey(User, null=True, blank=True,related_name='User_reviews',on_delete=SET_NULL)  # author_id, user_id [erd_cloud 통일]
    product = models.ForeignKey(Product, null=True, blank=True, related_name='Product_reviews',on_delete=SET_NULL)
    tasteContent = models.TextField()
    priceContent = models.TextField()
    convenienceContent = models.TextField()  # erd cloud 추가
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    reviewImageUrl = models.ImageField(upload_to='review/', null=True, blank=True, max_length=500)  # url, imageField, null, blank true
    recommender = models.ManyToManyField(User, null=True, blank=True,related_name='Review_recommender',through='ReviewRecommender')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어

class ReviewRecommender(models.Model):
    recommender = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, null=True, blank=True,on_delete=SET_NULL)
    recommended_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_recommender'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'tasteContent', 'priceContent', 'convenienceContent',
                  'reviewImageUrl']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'tasteContent': '맛 리뷰',
            'priceContent': '가격 리뷰',
            'convenienceContent': '편리성 리뷰',
            'product': '제품',
            'reviewImageUrl': '제품 사진',
        }


class PriceLog(models.Model):
    id = models.AutoField(primary_key=True)
    review=models.ForeignKey(Review, on_delete=models.CASCADE)
    reviewTokenize=models.CharField(max_length=200)
    PosNeg=models.IntegerField(null=False,default=0)
    Confidence=models.FloatField(null=False,default=0.0)

class TasteLog(models.Model):
    id = models.AutoField(primary_key=True)
    review=models.ForeignKey(Review, on_delete=models.CASCADE)
    reviewTokenize=models.CharField(max_length=200)
    PosNeg=models.IntegerField(null=False,default=1)
    Confidence=models.FloatField(null=False,default=0.0)
    sentence_id = models.IntegerField(null=False, default=0)

class ConvenienceLog(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    reviewTokenize = models.CharField(max_length=200)
    keybert_keywords = models.JSONField(default=list)
    top_sim_tags = models.JSONField(default=list)

    def __str__(self):
        return f"ConvenienceLog {self.id} - Review {self.review.id}"

class TasteKeywordLog(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    reviewTokenize = models.CharField(max_length=200)
    keybert_keywords = models.JSONField(default=list)
    top_sim_tags = models.JSONField(default=list)
    sentence_id = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f"ConvenienceLog {self.id} - Review {self.review.id}"
