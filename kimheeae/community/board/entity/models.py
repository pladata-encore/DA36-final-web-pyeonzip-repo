from django.db import models
from django import forms


# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=80, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

# form#
class BoardForm(forms.Form):

    class Meta:
        model = Board
        fields = ('title', 'contents')
        labels = {
            'title' : '제목',
            'content': '내용'
        }
