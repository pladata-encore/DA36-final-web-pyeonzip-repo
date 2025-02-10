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
    productId = models.AutoField(primary_key=True) #크롤링 후 수정 예정
    productName = models.CharField(max_length=100)
    convenientStoreName = models.IntegerField() #0,1,2,3
    productPrice = models.IntegerField()
    productImageUrl = models.URLField() #Imagefield 차이점 확인 후!! 
    updated_at = models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User, null=True, blank=True, related_name='Product_likes') # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어

class Review(models.Model):
    reviewId=models.AutoField(primary_key=True) # okay
    authorId = models.ForeignKey(User,null=True, blank=True, related_name='User_reviews') # author_id, user_id [erd_cloud 통일]
    productId=models.ForeignKey(Product,null=True, blank=True, related_name='Product_reviews')  
    tasteContent = models.TextField() 
    priceContent = models.TextField()
    convenienceContent=models.TextField() # erd cloud 추가
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    reviewImageUrl=models.URLField() # url, imageField
    recommender = models.ManyToManyField(User, null=True, blank=True, related_name='Review_voters')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어

class ReviewForm(forms.ModelForm):
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

class Category(models.Model):
    categoryId=models.AutoField(primary_key=True)
    categoryName=models.CharField(max_length=10)

class Community(models.Model):
    communityId=models.AutoField(primary_key=True)
    categoryId=models.ForeignKey(Category,null=True, blank=True)
    authorId = models.ForeignKey(User,null=True, blank=True, related_name='User_community')
    productId=models.ForeignKey(Product,null=True, blank=True, related_name='Product_reviews') # 3개가 참조 가능 ? ? ?  ? ?  
    communityTitle=models.CharField(max_length=100)
    communityContent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline=models.DateField()
    voter = models.ManyToManyField(User, null=True,blank=True,related_name='Community_voters')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['categoryId','communityTitle', 'communityContent','productId']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'categoryId' : '카테고리',
            'communityTitle': '제목',
            'communityContent': '내용',
            'productId' : '제품 선택',
    
        }
