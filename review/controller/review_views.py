from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from review.entity.models import ReviewForm, Review, ReviewRecommender
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


def review_recommender(request, review_id):
    review = get_object_or_404(Review, reviewId=review_id)
    user = request.user

    existing_recommendation = ReviewRecommender.objects.filter(recommender=user, review=review)

    if existing_recommendation.exists():
        existing_recommendation.delete()
        recommended = False
    else:
        ReviewRecommender.objects.create(recommender=user, review=review)
        recommended = True

    return JsonResponse({
        "recommended": recommended,
        "recommend_count": review.recommender.count()
    })