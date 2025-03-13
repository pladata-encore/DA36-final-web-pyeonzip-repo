from django.conf import settings
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from review.entity.models import ReviewForm, Review, ReviewRecommender, TasteLog, PriceLog, ConvenienceLog, \
    TasteKeywordLog
from review.service.review_service import ReviewServiceImpl
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse

from review.service.upload_service import S3Client
from review.service.sentiment_service import analyze_sentiment_taste, analyze_sentiment_cost
from review.service.keyword_service import extract_keywords

import re
import json
import requests
import os
# from konlpy.tag import Okt


review_service = ReviewServiceImpl()
s3_client = S3Client()

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


def preprocess_review_for_sentiment(text):
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
        taste_texts = preprocess_review_for_sentiment(review.tasteContent)
        price_texts = preprocess_review_for_sentiment(review.priceContent)
        print(f"🔹 [Django] 분석 요청: {taste_texts, price_texts}")

        # ✅ AI 추론 요청
        taste_results = analyze_sentiment_taste(taste_texts)
        price_results = analyze_sentiment_cost(price_texts)
        print(f"🔹 [Django] FastAPI 응답: {taste_results, price_texts}")

        # ✅ DB 저장 (TasteLog, PriceLog)
        # for text, result in zip(taste_texts, taste_results):
        #     TasteLog.objects.create(
        #         review=review,
        #         reviewTokenize=text,
        #         PosNeg=result["PosNeg"],
        #         Confidence=result["Confidence"]
        #     )

        for idx, (text, result) in enumerate(zip(taste_texts, taste_results)):
            TasteLog.objects.create(
                review=review,
                reviewTokenize=text,
                sentence_id=idx,  # sentence_id 추가
                PosNeg=result["PosNeg"],
                Confidence=result["Confidence"]
            )

        for text, result in zip(price_texts, price_results):
            PriceLog.objects.create(
                review=review,
                reviewTokenize=text,
                PosNeg=result["PosNeg"],
                Confidence=result["Confidence"]
            )

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


# okt = Okt()

# MEDIAFILES 내 stopwords 파일 경로
stopword_file = os.path.join(settings.MEDIA_ROOT, "reviews\\stopwords.txt")

def load_stopwords(filepath):
    with open(filepath, 'r', encoding='CP949') as f:
        stopwords = set(f.read().strip().split(","))
    return stopwords

stopwords = load_stopwords(stopword_file)

# ✅ 텍스트 정제 및 불용어 제거
def preprocess_review_for_keyword(review, stopwords):
    cleaned_review = re.sub(r"[^가-힣\s]", "", review)
    words = okt.morphs(cleaned_review)
    filtered_words = [word for word in words if word not in stopwords]  # 불용어 제거
    return " ".join(filtered_words)

@require_POST
@csrf_exempt
# ✅ 리뷰 전처리 및 키워드 추출 + DB 저장
def analyze_review_keyword(request):
    try:
        data = json.loads(request.body)
        review_id = data.get("review_id")

        # ✅ 리뷰 가져오기
        review = Review.objects.get(reviewId=review_id)

        # ✅ 리뷰 데이터 전처리
        conv_texts = preprocess_review_for_keyword(review.convenienceContent, stopwords)
        print(f"🔹 [Django] 분석 요청: {conv_texts}")
        taste_texts = preprocess_review_for_sentiment(review.tasteContent)
        print(f"🔹 [Django] 분석 요청: {taste_texts}")

        # ✅ AI 추론 요청
        keyword_result = extract_keywords(conv_texts)
        print(f"🔹 [Django] FastAPI 응답: {keyword_result}")
        # for taste_text in taste_texts:
        #     keyword_result_taste = extract_keywords(taste_text)
        #     TasteKeywordLog.objects.create(
        #         review=review,
        #         reviewTokenize=taste_texts,
        #         keybert_keywords=keyword_result_taste["keybert_keywords"],
        #         top_sim_tags=keyword_result_taste["top_sim_tags"]
        #     )
        for idx, taste_text in enumerate(taste_texts):
            keyword_result_taste = extract_keywords(taste_text)
            TasteKeywordLog.objects.create(
                review=review,
                reviewTokenize=taste_text,
                sentence_id=idx,  # sentence_id 추가
                keybert_keywords=keyword_result_taste["keybert_keywords"],
                top_sim_tags=keyword_result_taste["top_sim_tags"]
            )
            print(keyword_result_taste)

        # ✅ DB 저장 (ConvenienceLog 모델에 저장)
        ConvenienceLog.objects.create(
            review=review,
            reviewTokenize=conv_texts,
            keybert_keywords=keyword_result["keybert_keywords"],
            top_sim_tags=keyword_result["top_sim_tags"]
            )

        return JsonResponse({
            "message": "Keyword analysis completed",
            "review_id": review_id
        }, status=200)

    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
