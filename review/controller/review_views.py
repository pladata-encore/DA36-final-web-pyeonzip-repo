from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from review.entity.models import ReviewForm, Review, ReviewRecommender, TasteLog, PriceLog
from review.service.review_service import ReviewServiceImpl
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse

from review.service.upload_service import S3Client
from review.service.sentiment_service import analyze_sentiment
import re
import os
import json
import requests

review_service = ReviewServiceImpl()
s3_client = S3Client()

def review_main(request):
    return render(request, 'review/review_main.html', {'review_main':review_main})


@login_required(login_url='users:login')
def review_write(request):
    product_id = request.GET.get("product_id", "")  # GET 요청에서 product_id 가져오기

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author_id=request.user.id

            if 'reviewImageUrl' in request.FILES:
                obj_url = s3_client.upload_review_image(request.FILES['reviewImageUrl'])
                if obj_url:
                    review.reviewImageUrl = obj_url

            product_id = request.POST.get("product_id")
            if product_id:
                review.product_id = product_id
            review_service.create(review)
            return redirect('product:product_detail', product_id=product_id)
        else:
            print('form.errors=',form.errors)
    else:
        form = ReviewForm()

    return render(request, 'review/review_form.html', {'form': form, 'product_id': product_id})


@login_required(login_url='users:login')
def review_recommend(request, review_id):
    review = review_service.find_by_review_id(review_id)
    if request.user.id == review.author_id:
        return JsonResponse({
            'result': 'false'
        })
    try:
        review,recommended = review_service.add_remove_recommend(review_id, request.user)
        recommender_count = review.recommender.count() if hasattr(review, 'recommender') else 0

        print('product.recommender_count() =', recommender_count)
        return JsonResponse({
            'result': 'success',
            'recommender_count': recommender_count,
            'recommended':recommended
        })
    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'message': str(e)
        }, status=400)


def preprocess_review(text):
    if not text:
        return []

    # ✅ \n 기준으로 분리 후 explode
    reviews = text.split('\n')
    cleaned_reviews = []

    for review in reviews:
        review = review.strip()  # 양쪽 공백 제거
        if not review:
            continue

        # ✅ 숫자, 영어, 특수문자 제거
        review = re.sub(r"[0-9a-zA-Z]", "", review)
        review = re.sub(r"[.,~!@#$%^&*()_+=\-{}\[\]:;'<>,?/|\\]", "", review)

        # ✅ 정규식을 활용한 추가 분리
        split_words = ['요 ', '용 ', '다 ', '데 ', '만 ', 'ㅎ ', 'ㅋ ']
        pattern = '|'.join(f'(?<={re.escape(word)})' for word in split_words)
        review_parts = re.split(pattern, review)

        # ✅ 공백 제거 후 추가
        for part in review_parts:
            part = part.strip()
            if part:
                cleaned_reviews.append(part)

    return cleaned_reviews



# ✅ Django API 엔드포인트 (리뷰 감성 분석 및 DB 저장)
@require_POST
@csrf_exempt
def analyze_review_sentiment(request):
    try:
        data = json.loads(request.body)
        review_id = data.get("review_id")

        # ✅ 리뷰 가져오기
        review = Review.objects.get(reviewId=review_id)

        # ✅ 리뷰 데이터 전처리
        taste_texts = preprocess_review(review.tasteContent)
        # price_texts = preprocess_review(review.priceContent)
        # conv_texts = preprocess_review(review.convenienceContent)
        print(f"🔹 [Django] 분석 요청: {taste_texts}")

        # ✅ AI 추론 요청
        taste_results = analyze_sentiment(taste_texts)
        # price_results = analyze_sentiment(price_texts)
        # conv_results = analyze_sentiment(conv_texts)
        print(f"🔹 [Django] FastAPI 응답: {taste_results}")

        # ✅ DB 저장 (TasteLog, PriceLog, ConvLog)
        for text, result in zip(taste_texts, taste_results):
            TasteLog.objects.create(
                review=review,
                reviewTokenize=text,
                PosNeg=result["PosNeg"],
                Confidence=result["Confidence"]
            )

        # for text, result in zip(price_texts, price_results):
        #     PriceLog.objects.create(
        #         review=review,
        #         reviewTokenize=text,
        #         PosNeg=result["PosNeg"],
        #         Confidence=result["Confidence"]
        #     )
        #
        # for text, result in zip(conv_texts, conv_results):
        #     ConvLog.objects.create(
        #         review=review,
        #         reviewTokenize=text,
        #         PosNeg=result["PosNeg"],
        #         Confidence=result["Confidence"]
        #     )

        return JsonResponse({
            "message": "Sentiment analysis completed",
            "review_id": review_id
        }, status=200)

    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



