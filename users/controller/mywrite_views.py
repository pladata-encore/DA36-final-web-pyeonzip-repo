from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from review.entity.models import Review
from review.service.review_service import ReviewServiceImpl
from users.entity.models import UserDetail

review_service = ReviewServiceImpl.get_instance()

@login_required(login_url="user:login")
def mywrite(request):
    author=UserDetail.objects.get(user_id=request.user.id)
    my_reviews = review_service.find_by_user_id(author)
    # print(request.user.id)
    # print(author)
    return render(request, 'users/mywrite.html', {'my_reviews': my_reviews})
