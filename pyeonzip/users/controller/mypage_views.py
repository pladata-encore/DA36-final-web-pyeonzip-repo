from django.shortcuts import redirect, render

from review.entity.models import ReviewForm
from users.entity.mypage_models import MyPage


def mypage(request):
    if request.method == 'POST':
        form = MyPage(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pass
        else:
            print(form.errors)
    return render(request, 'users/mypage.html', {'mypage':MyPage})