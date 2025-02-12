from django.db import models
from django.forms import forms


# Create your models here.
class Review(models.Model):
    # reviewId=models.AutoField(primary_key=True) # okay
    # authorId = models.ForeignKey(User,null=True, blank=True, related_name='User_reviews') # author_id, user_id [erd_cloud 통일]
    # productId=models.ForeignKey(Product,null=True, blank=True, related_name='Product_reviews')
    tasteContent = models.TextField()
    priceContent = models.TextField()
    convenienceContent=models.TextField() # erd cloud 추가
    created_at = models.DateTimeField(auto_now_add=True)
    # modified_at = models.DateTimeField(auto_now=True)
    reviewImageUrl=models.URLField() # url, imageField
    # recommender = models.ManyToManyField(User, null=True, blank=True, related_name='Review_voters')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어



class ReviewForm(forms.Form):
    class Meta:
        model = Review
        fields = ['productId','tasteContent', 'priceContent','convenienceContent','reviewImageUrl']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'tasteContent': '맛 리뷰',
            'priceContent': '가격 리뷰',
            'convenienceContent':'편리성 리뷰',
            'productId' : '제품',
            'reviewImageUrl' : '제품 사진',
        }