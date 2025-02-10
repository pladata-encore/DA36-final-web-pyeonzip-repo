from django.db import models
from django.forms import ModelForm


# Create your models here.
class Review(models.Model):
    f_content = models.TextField(max_length=200)
    p_content = models.TextField(max_length=200)
    e_content = models.TextField(max_length=200)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('f_content', 'p_content','e_content', 'image')
        labels = {
            'f_content': '맛',
            'p_content': '가격',
            'e_content': '기타',
            'image' : '사진'
        }