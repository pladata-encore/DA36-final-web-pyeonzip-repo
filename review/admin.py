import json
import requests
from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.http import JsonResponse
from datetime import datetime
from django.utils.timezone import make_aware
from review.entity.models import Review

# Django API 엔드포인트
API_URL_SENTIMENT = "http://127.0.0.1:8000/review/analyze_review/"
API_URL_KEYWORD = "http://127.0.0.1:8000/review/analyze_review_keyword/"

@admin.action(description="선택한 리뷰의 감성 분석 실행")
def analyze_selected_reviews_sentiment(modeladmin, request, queryset):
    """
    선택한 리뷰에 대해 감성 분석 API 호출
    """
    success_count = 0
    fail_count = 0
    for review in queryset:
        payload = {"review_id": review.reviewId}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(API_URL_SENTIMENT, json=payload, headers=headers)
            response_json = response.json()

            # ✅ 예상 응답 형식 확인 후 메시지 출력
            if response.status_code == 200:
                messages.success(request, f"✅ 리뷰 {review.reviewId} 감성 분석 성공!")
                success_count += 1
            else:
                error_msg = response_json.get("error", "알 수 없는 오류")
                messages.error(request, f"🚨 리뷰 {review.reviewId} 감성 분석 실패: {error_msg}")
                fail_count += 1

        except requests.exceptions.RequestException as e:
            messages.error(request, f"🚨 API 요청 실패 (리뷰 {review.reviewId}): {str(e)}")
            fail_count += 1

    messages.info(request, f"📊 감성 분석 완료: 성공 {success_count}건, 실패 {fail_count}건")


@admin.action(description="선택한 리뷰의 키워드 분석 실행")
def analyze_selected_reviews_keyword(modeladmin, request, queryset):
    """
    선택한 리뷰에 대해 키워드 분석 API 호출
    """
    success_count = 0
    fail_count = 0
    for review in queryset:
        payload = {"review_id": review.reviewId}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(API_URL_KEYWORD, json=payload, headers=headers)
            response_json = response.json()

            # ✅ 예상 응답 형식 확인 후 메시지 출력
            if response.status_code == 200:
                messages.success(request, f"✅ 리뷰 {review.reviewId} 키워드 분석 성공!")
                success_count += 1
            else:
                error_msg = response_json.get("error", "알 수 없는 오류")
                messages.error(request, f"🚨 리뷰 {review.reviewId} 키워드 분석 실패: {error_msg}")
                fail_count += 1

        except requests.exceptions.RequestException as e:
            messages.error(request, f"🚨 API 요청 실패 (리뷰 {review.reviewId}): {str(e)}")
            fail_count += 1

    messages.info(request, f"📊 키워드 분석 완료: 성공 {success_count}건, 실패 {fail_count}건")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewId", "author", "created_at", "modified_at")
    actions = [analyze_selected_reviews_sentiment, analyze_selected_reviews_keyword]


admin.site.register(Review, ReviewAdmin)