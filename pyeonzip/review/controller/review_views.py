from django.shortcuts import redirect, render

from review.entity.models import ReviewForm


def review_write(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            pass


    return render(request, 'review_/review_write.html', {'ReviewForm': ReviewForm})
