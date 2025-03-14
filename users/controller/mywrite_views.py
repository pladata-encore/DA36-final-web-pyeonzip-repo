from allauth.core.internal.httpkit import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from community.service.community_service import CommunityServiceImpl
from review.service.review_service import ReviewServiceImpl
from users.entity.models import UserDetail
from django.contrib import messages
from django.http import JsonResponse




review_service = ReviewServiceImpl.get_instance()
community_service = CommunityServiceImpl.get_instance()
@login_required()
def my_review(request):
    my_reviews = review_service.find_by_user_id(request.user.id)
    for review in my_reviews:
        review.recommend_count = review.recommender.count()
        review.author_nickname = review.author.userdetail.nickname if review.author.userdetail else "익명"
        review.author_profile = review.author.userdetail.profile if review.author.userdetail and review.author.userdetail.profile else None

    # user = UserDetail.objects.filter(user_id=request.user.id).first()
    # user_profile = user.profile.url if user and user.profile else None

    return render(request, 'users/my_review.html', {'my_reviews': my_reviews})

@login_required()
def review_delete(request, review_id):
    del_review = review_service.delete(review_id)
    messages.success(request, '리뷰를 삭제했습니다.', extra_tags="review_delete")

    return redirect('users:my_review')

@login_required()
def my_community(request):
    author = UserDetail.objects.get(user_id=request.user.id)
    my_communities = community_service.find_by_user_id(author)

    return render(request, 'users/my_community.html', {'my_communities': my_communities})

