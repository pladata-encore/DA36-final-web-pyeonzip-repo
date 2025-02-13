from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255,null=False,unique=True,default='unknown')
    product_category_name=models.CharField(max_length=255,null=False,default='unknown')
    convenient_store_name = models.IntegerField(null=False,default=0)  # 0,1,2,3
    product_price = models.IntegerField(null=False,default=0)
    product_image_url = models.CharField(max_length=500,null=False,default='unknown')
    updated_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, null=True, blank=True,related_name='Product_likes',through='ProductLikes')  # 투표일 추가 가능인지 check , 불가능일 시 : model 따로 만들어

class ProductLikes(models.Model):
    userID=models.ForeignKey(User, on_delete=models.CASCADE)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    liked_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Product_likes'

