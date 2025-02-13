from django.shortcuts import redirect, render

from review.entity.models import ReviewForm
from users.entity.models import mypageUpdateForm


def mypage_update(request):
    if request.method == 'POST':
        form = mypageUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pass
        else:
            print(form.errors)
    return render(request, 'users/mypage.html', {'mypage':mypageUpdateForm})