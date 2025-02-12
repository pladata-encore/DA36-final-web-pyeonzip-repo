from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL

class ProductCategory(models.Model):
    productCategoryId = models.AutoField(primary_key=True)
    productCategoryName = models.CharField(max_length=100)

class Product(models.Model):
    productId = models.AutoField(primary_key=True)  # 크롤링 후 수정 예정
    productName = models.CharField(max_length=100)
    productCategoryId=models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    convenientStoreName = models.IntegerField()  # 0,1,2,3
    productPrice = models.IntegerField()
    productImageUrl = models.URLField()  # Imagefield 차이점 확인 후!!
    updated_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, null=True, blank=True,related_name='Product_likes',through='ProductLikes')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어

class ProductLikes(models.Model):
    userID=models.ForeignKey(User, on_delete=models.CASCADE)
    productId = models.ForeignKey(Product, null=True, blank=True,on_delete=SET_NULL)
    liked_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Product_likes'
