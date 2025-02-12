from django.shortcuts import render

from review.entity.models import ReviewForm


# Create your views here.
def index(request):
    return render(request, 'main.html')

def review_write(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # form.save()
            pass

        print(request.POST)
    return render(request, 'review/review_form.html', {ReviewForm:ReviewForm})