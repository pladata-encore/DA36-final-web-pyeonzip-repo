from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from community.entity.models import CommunityForm, Community
from community.service.community_service import CommunityServiceImpl
from users.entity.models import UserDetail

community_service = CommunityServiceImpl()

def community_list(request):
    communities = community_service.find_all().order_by('-created_at')
    return render(request, 'community/community_list.html', {'communities': communities })

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

@login_required(login_url='users:login')
def vote_community(request):
    """ 투표하기 기능 (AJAX 요청)"""
    if request.method == 'POST':
        from json import loads
        data = loads(request.body)
        community_id = data.get("communityId")

        if not community_id:
            return JsonResponse({"success": False, "message": "커뮤니티 ID 없음"}, status=400)

        is_voted = community_service.add_vote(community_id, request.user)

        if is_voted:
            return JsonResponse({"success": True, "message": "✅ 투표 완료!"})
        else:
            return JsonResponse({"success": False, "message": "❌ 이미 투표한 게시글입니다."})

    return JsonResponse({"success": False, "message": "잘못된 요청"}, status=400)

@login_required(login_url='users:login')
def community_detail(request, communityId):
    community = get_object_or_404(Community.objects.prefetch_related("products", "voter"), communityId=communityId)
    return render(request, 'community/community_detail.html', {'community': community})
