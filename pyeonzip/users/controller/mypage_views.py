from django.shortcuts import redirect, render

from review.entity.models import ReviewForm
from users.entity.models import MypageUpdateForm, UserDetail


def mypage_update(request):
    user_detail = UserDetail.objects.get(user=request.user)

    if request.method == 'POST':
        form = MypageUpdateForm(request.POST, request.FILES, instance=user_detail)
        if form.is_valid():
            form.save()
            return redirect('users:mypage')

    else:
        form = MypageUpdateForm(instance=user_detail)

    return render(request, 'users/mypage_update.html', {'form':form})


def mypage(request):
    user_detail = UserDetail.objects.get(user=request.user)
    return render(request, 'users/mypage.html', {
        'user_detail':user_detail,
        'nickname' : user_detail.nickname,
        'email' : user_detail.email,})