from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from community.service.community_service import CommunityServiceImpl
from review.service.review_service import ReviewServiceImpl
from users.entity.models import UserDetail
from django.contrib.auth.models import User


review_service = ReviewServiceImpl.get_instance()
community_service = CommunityServiceImpl.get_instance()
@login_required()
def my_review(request):
    author=UserDetail.objects.get(user_id=request.user.id)
    my_reviews = review_service.find_by_user_id(author)
    # print(request.user.id)
    # print(author)
    return render(request, 'users/my_review.html', {'my_reviews': my_reviews})

@login_required()
def my_community(request):
    author = UserDetail.objects.get(user_id=request.user.id)
    my_communities = community_service.find_by_user_id(author)
    return render(request, 'users/my_community.html', {'my_communities': my_communities})


