from django.db import models
from django.forms import forms


# Create your models here.

class Community(models.Model):
    communityId = models.AutoField(primary_key=True)
    # categoryId = models.ForeignKey(Category, null=True, blank=True)
    # authorId = models.ForeignKey(User, null=True, blank=True, related_name='User_community')
    # productId = models.ForeignKey(Product, null=True, blank=True, related_name='Product_reviews')  # 3개가 참조 가능 ? ? ?  ? ?
    communityTitle = models.CharField(max_length=100)
    communityContent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    # voter = models.ManyToManyField(User, null=True, blank=True,related_name='Community_voters')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어


class CommunityForm(forms.Form):
    class Meta:
        model = Community
        fields = ['categoryId', 'communityTitle', 'communityContent', 'productId']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'categoryId': '카테고리',
            'communityTitle': '제목',
            'communityContent': '내용',
            'productId': '제품 선택',

        }
