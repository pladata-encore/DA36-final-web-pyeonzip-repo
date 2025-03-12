from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.timezone import now
from json import loads

from community.entity.models import CommunityForm, Community
from community.service.community_service import CommunityServiceImpl
from users.entity.models import UserDetail


community_service = CommunityServiceImpl()

def community_list(request):
    communities = community_service.find_all().order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(communities, 5)
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages

    if request.user.id is not None:
        left_post, right_post = community_service.get_random_unvoted_posts(request.user)
    else:
        left_post, right_post = None, None
    for community in communities:
        community.is_expired = community.deadline < now().date()  # 마감 여부 계산
    print(request.user.id)
    return render(request, 'community/community_list.html', {'page_obj': page_obj,'last_page':last_page, 'left_post': left_post,
        'right_post': right_post })

@login_required(login_url='users:login')
def community_write(request):
    if request.method == 'POST':
        return redirect("community:community_save") # 🔹 폼이 제출되면 community_save로 이동
    else:
        form = CommunityForm()
        return render(request, 'community/community_form.html', {'CommunityForm': form})

@login_required(login_url='users:login')
def community_save(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            products = form.cleaned_data['products']
            product_ids = [product.product_id for product in products]

            user_detail = UserDetail.objects.get(user_id=request.user.id)

            community_service.create_community(form.cleaned_data, product_ids, user_detail)
            return redirect("community:community_list")

        else:
            print('form.errors=', form.errors)

    return redirect("community:community_write")


def vote_community(request):
    """ 투표하기 기능 (AJAX 요청)"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "로그인 후 투표 가능합니다", "redirect": "/users/login"}, status=401)

        data = loads(request.body)
        community_id = data.get("communityId")

        if not community_id:
            return JsonResponse({"success": False, "message": "커뮤니티 ID 없음"}, status=400)
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return JsonResponse({"success": False, "message": "존재하지 않는 커뮤니티 게시글"}, status=404)

        if community.deadline < now().date():
            return JsonResponse({"success": False, "message": "❌ 투표 기간이 종료되었습니다."}, status=400)

        is_voted = community_service.add_vote(community_id, request.user)

        if is_voted:
            return JsonResponse({"success": True, "message": " 소중한 투표 감사합니다.😊","vote_count": community.voter.count()})
        else:
            return JsonResponse({"success": False, "message": " 이미 투표한 게시글입니다."})

    return JsonResponse({"success": False, "message": "잘못된 요청"}, status=400)

@login_required(login_url='users:login')
def community_detail(request, communityId):
    community = get_object_or_404(Community.objects.prefetch_related("products", "voter"), communityId=communityId)
    community.is_expired = community.deadline < now().date()  # 마감 여부 계산

    return render(request, 'community/community_detail.html', {'community': community})
