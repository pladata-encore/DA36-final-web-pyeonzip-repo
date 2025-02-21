from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from review.entity.models import ReviewForm
from review.service.review_service import ReviewServiceImpl
from django.http import JsonResponse

review_service = ReviewServiceImpl()
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


@login_required()
def review_recommender(request, review_id):
    try:
        review, recommended = review_service.review_recommenders(review_id, request.user)
        recommenders_count = review.recommenders.count() if hasattr(review, 'recommenders') else 0

        print('review.recommenders.count() =', recommenders_count)
        return JsonResponse({
            'result': 'success',
            'recommenders_count': recommenders_count,
            'recommended': recommended,
        })
    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'message': str(e)
        }, status=400)

