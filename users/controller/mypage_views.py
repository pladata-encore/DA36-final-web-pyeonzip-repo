from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import re

from product.entity.models import Product, ProductLikes
from review.entity.models import ReviewForm
from users.controller.views import login
from users.entity.models import MypageUpdateForm, UserDetail
from django.contrib.auth.models import User
from django.http import JsonResponse

def mypage_update(request):
    user_detail = UserDetail.objects.get(user=request.user)

    if request.method == 'POST':
        form = MypageUpdateForm(request.POST, request.FILES, instance=user_detail)

        if form.is_valid():
            nickname = form.cleaned_data.get("nickname") # 입력된 닉네임 가져오기

            # 닉네임 중복체크
            if UserDetail.objects.filter(nickname=nickname).exclude(id=request.user.id).exists():
                form.add_error('nickname', f'이미 사용 중인 닉네임입니다.')
            else:
                form.save()
                return redirect('users:mypage')

    else:
        form = MypageUpdateForm(instance=user_detail)

    return render(request, 'users/mypage_update.html', {'form':form})

def mypage(request):
    user = request.user # 접속한 유저
    user_detail = UserDetail.objects.get(user=request.user)

    liked_product_ids = ProductLikes.objects.filter(user=user).values_list('product_id', flat=True)
    liked_products = Product.objects.filter(product_id__in=liked_product_ids) # 현재 유저가 좋아요 한 상품

    return render(request, 'users/mypage.html', {
        'user_detail': user_detail,
        'nickname' : user_detail.nickname,
        'email' : user_detail.email,
        'liked_products':liked_products
    })


def check_nickname_duplicate(request):
    nickname = request.GET.get('nickname','')

    # 닉네임 유효성 검사
    nickname_pattern = r'^[A-Za-z0-9_]{8,20}$'

    if not nickname:
        return JsonResponse({'error':'닉네임을 입력하세요.'}, status=400)

    if not re.match(nickname_pattern, nickname):
        return JsonResponse({'error' : '닉네임은 영어 대소문자, 숫자, 특수문자_ 만 사용 가능합니다.'})

    # DB에 중복된 닉네임 있는지 확인
    exists = UserDetail.objects.filter(nickname=nickname).exists()

    return JsonResponse({'exists': exists})

