from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import re

from django.contrib import messages
from product.entity.models import Product, ProductLikes
from review.entity.models import ReviewForm
from users.controller.views import login
from users.entity.models import MypageUpdateForm, UserDetail
from django.contrib.auth.models import User
from django.http import JsonResponse

def mypage_update(request):
    user_detail = UserDetail.objects.get(user=request.user)  # 현재 로그인한 유저의 UserDetail 가져오기

    if request.method == 'POST':
        form = MypageUpdateForm(request.POST, request.FILES, instance=user_detail)

        if form.is_valid():
            nickname_changed = 'nickname' in form.changed_data  # 닉네임 변경 여부 확인
            profile_changed = 'profile' in form.changed_data  # 프로필 변경 여부 확인

            # 프로필 삭제 처리
            if 'profile-clear' in request.POST: # Django의 파일 필드 삭제
                user_detail.profile = None # 기본이미지로 변경
                profile_changed = True # 프로필 이미지 변경됨

            if nickname_changed:
                nickname = form.cleaned_data.get("nickname")  # 입력된 닉네임 가져오기

                # 🚀 닉네임 중복 체크 (현재 로그인한 유저는 제외)
                if UserDetail.objects.filter(nickname=nickname).exclude(user=request.user).exists():
                    form.add_error('nickname', '이미 사용 중인 닉네임입니다.')  # 오류 메시지 추가
                else:
                    user_detail.nickname = nickname  # 닉네임 업데이트

            if profile_changed and 'profile-clear'  not in request.POST:
                user_detail.profile = form.cleaned_data.get("profile")  # 프로필 사진 업데이트

            # 🚀 닉네임이나 프로필 사진이 변경되었을 경우 저장
            if nickname_changed or profile_changed:
                user_detail.save()
                messages.success(request, "변경 사항이 저장되었습니다.")  # 저장 완료 메시지 추가
                return redirect('users:mypage')

            else:
                form.add_error(None, "변경된 내용이 없습니다.")  # 변경 사항이 없을 경우 오류 추가

    else:
        form = MypageUpdateForm(instance=user_detail)

    return render(request, 'users/mypage_update.html', {'form': form, 'user_detail':user_detail})

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

