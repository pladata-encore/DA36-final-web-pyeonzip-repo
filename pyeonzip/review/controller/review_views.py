from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from review.entity.models import ReviewForm

def review_main(request):
    return render(request, 'review/review_main.html', {'review_main':review_main})

@login_required(login_url='users:login')
def review_write(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pass
        else:
            print('form.errors=',form.errors)
    else:
        form = ReviewForm()

    return render(request, 'review/review_form.html', {'ReviewForm': ReviewForm})
