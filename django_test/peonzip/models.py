from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


### Models ###
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ageRange = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    reward = models.CharField(max_length=100)
    # 확장하고자하는 사용자 필드
    email = models.EmailField(label='Email')
    gender=models.BooleanField(label='Gender', required=False)
    birthday = models.DateField(null=True, blank=True)  # null(DB 테이블/컬럼), blank(Form validation)
    profile = models.ImageField(upload_to='profile/',null=True, blank=True)


### Forms ###
class UserForm(UserCreationForm):
    """
    UserCreationForm은 username, password1, password2 필드 제공
    """
    nickname= forms.CharField(label='Nickname',required=False)
    birthday = forms.DateField(label='Birthday', required=False)
    gender=forms.BooleanField(label='Gender', required=False)
    profile = forms.ImageField(label='Profile', required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name','phoneNumber')

class Product(models.Model):
    productId = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=100)
    convenientStoreName = models.IntegerField()
    productPrice = models.IntegerField()
    productImageUrl = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    reviewId=models.AutoField(primary_key=True)
    author = models.ForeignKey(User,null=True, blank=True, related_name='User_reviews')
    productId=models.ForeignKey(Product,null=True, blank=True, related_name='Product_reviews')
    tasteContent = models.TextField()
    priceContent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    profileUrl=models.URLField()
    voter = models.ManyToManyField(User, null=True, blank=True, related_name='review_voters')  # 추천인 추가

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['tasteContent', 'priceContent']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'subject': '맛 리뷰',
            'content': '가격 리뷰',
        }

class Category(models.Model):
    categoryId=models.AutoField(primary_key=True)
    categoryName=models.CharField(max_length=100)

class Community(models.Model):
    communityId=models.AutoField(primary_key=True)
    categoryId=models.ForeignKey(Category,null=True, blank=True)
    author = models.ForeignKey(User,null=True, blank=True, related_name='User_community')
    productId=models.ForeignKey(Product,null=True, blank=True, related_name='Product_reviews')
    communityTitle=models.CharField(max_length=100)
    communityContent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline=models.DateField()
    voter = models.ManyToManyField(User, null=True,blank=True,related_name='community_voters')  # 추천인 추가


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['communityTitle', 'communityContent']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'subject': '제목',
            'content': '내용',
        }
