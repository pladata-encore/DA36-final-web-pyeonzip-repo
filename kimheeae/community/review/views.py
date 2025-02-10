from django.shortcuts import redirect

from review.models import ReviewForm


def review_write(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect('review_write')
