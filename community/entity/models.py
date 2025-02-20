from datetime import timedelta
from django.utils.timezone import now

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL
from product.entity.models import Product
from users.entity.models import UserDetail


class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=10)


class Community(models.Model):
    communityId = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, null=True, blank=True,on_delete=SET_NULL)
    author = models.ForeignKey(UserDetail, null=True, blank=True, related_name='User_community',on_delete=SET_NULL)
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

    def add_vote(self, user):
        """ 한 번 투표하면 취소할 수 없음"""
        if not CommunityVoters.objects.filter(community=self, voter=user).exists():  # 이미 투표한 경우 무시
            CommunityVoters.objects.create(community=self, voter=user)  # 투표 추가
            return True  # ✅ 투표 성공
        return False  # ❌ 이미 투표한 경우 아무 작업 없음


class CommunityVoters(models.Model):
    voter = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, null=True, blank=True,on_delete=SET_NULL)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_voters'
        unique_together = ('voter', 'community')

class CommunityForm(forms.ModelForm):
    products = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Community
        fields = ['category', 'communityTitle', 'communityContent', 'products']  # Form클래스에서 사용할 Model클래스 속성

        labels = {
            'category': '카테고리',
            'communityTitle': '제목',
            'communityContent': '내용',
            'products': '제품 선택',
        }
    def clean_products(self):
        """쉼표로 구분된 product_ids를 리스트로 변환하여 검증"""
        data = self.cleaned_data['products']
        if data:
            try:
                product_ids = [int(pid) for pid in data.split(",") if pid]  # ✅ 쉼표로 구분된 문자열을 리스트로 변환
                products = Product.objects.filter(product_id__in=product_ids)  # ✅ 유효한 제품 ID인지 확인
                return products  # ✅ 검증된 Product 객체 리스트 반환
            except ValueError:
                raise forms.ValidationError("유효한 제품 ID를 입력하세요.")
        return []




