from django.contrib import auth,messages
from django.shortcuts import render, redirect
from django.http import JsonResponse

from community.entity.models import CommunityForm
from oauth.entity.models import Mypagereview
from review.entity.models import ReviewForm


# from oauth.entity.models import UserForm
# from oauth.service.uauth_service import UAuthServiceImpl

# oauth_service=OAuthServiceImpl.get_instance()

def index(request):
    pass

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')


def mypage_review(request):
    if request.method == 'POST':
        form = Mypagereview(request.POST)
        if form.is_valid():
            # form.save()
            pass

        print(request.POST)
    return render(request, 'mypage/mypage_review.html', {ReviewForm:ReviewForm})

def mypage_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save(
            pass

        print(request.POST)

    return render(request,'mypage/mypage_community.html',{'CommunityForm':CommunityForm})

