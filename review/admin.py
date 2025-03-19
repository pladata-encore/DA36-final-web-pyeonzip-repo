import json
import requests
import csv
from django.http import HttpResponse
from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.http import JsonResponse
from datetime import datetime
from django.utils.timezone import make_aware
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from product.entity.models import Product
from review.entity.models import Review, TasteLog, PriceLog, ConvenienceLog, ReviewRecommender

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

# @admin.action(description="선택한 항목을 CSV로 내보내기")
# def export_as_csv(modeladmin, request, queryset):
#     """선택한 리뷰 데이터를 CSV 파일로 내보냄"""
#
#     # CSV 응답 설정
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="reviews_export.csv"'
#
#     writer = csv.writer(response)
#
#     # CSV 헤더 작성
#     writer.writerow(["ReviewId", "상품명", "편의점", "리뷰 내용", "맛 평가", "가격 평가", "키워드 평가", "Created At"])
#
#     # 선택한 리뷰 ID 목록 생성 (queryset에서 reviewId만 추출)
#     selected_review_ids = set(queryset.values_list('reviewId', flat=True))
#
#     # Django Admin의 queryset은 원래 Model 객체 리스트이므로, 가공된 데이터로 변환해야 함
#     expanded_reviews = modeladmin.get_queryset(request)
#
#     # 데이터 작성
#     for review in expanded_reviews:
#         if review["review"].reviewId in selected_review_ids:  # 선택한 데이터만 필터링
#             writer.writerow([
#                 review["review"].reviewId,
#                 review["review"].product.product_name if review["review"].product else "-",
#                 review["review"].product.convenient_store_name if review["review"].product else "-",
#                 review["review_content"],
#                 review["sentiment_analysis_taste"],
#                 review["sentiment_analysis_cost"],
#                 review["keyword_evaluation"],
#                 review["review"].created_at.strftime("%Y-%m-%d %H:%M"),
#             ])
#
#     return response

# ✅ 편의점 필터 추가
class ConvenientStoreFilter(admin.SimpleListFilter):
    title = '편의점'
    parameter_name = 'convenient_store'

    def lookups(self, request, model_admin):
        return [('GS25', 'GS25'), ('CU', 'CU'), ('7-ELEVEN', '7-ELEVEN')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(product__convenient_store_name=self.value())
        return queryset


# ✅ 감성 필터 추가
class SentimentFilter(admin.SimpleListFilter):
    title = '감성 분석 상태'
    parameter_name = 'sentiment'

    def lookups(self, request, model_admin):
        return [
            ('평가 전', '평가 전'),
            ('평가 완료', '평가 완료')
        ]

    def queryset(self, request, queryset):
        if self.value() == '평가 전':
            return queryset.exclude(
                reviewId__in=TasteLog.objects.values_list('review', flat=True)
            ).exclude(
                reviewId__in=PriceLog.objects.values_list('review', flat=True)
            )
        elif self.value() == '평가 완료':
            return queryset.filter(
                reviewId__in=TasteLog.objects.values_list('review', flat=True)
            )
        return queryset

# ✅ 키워드 필터 추가
class KeywordFilter(admin.SimpleListFilter):
    title = '키워드 분석 상태'
    parameter_name = 'keyword_evaluation'

    def lookups(self, request, model_admin):
        return [
            ('평가 전', '평가 전'),
            ('평가 완료', '평가 완료')
        ]

    def queryset(self, request, queryset):
        if self.value() == '평가 완료':
            return queryset.filter(
                reviewId__in=ConvenienceLog.objects.values_list('review_id', flat=True)
            )
        elif self.value() == '평가 전':
            return queryset.exclude(
                reviewId__in=ConvenienceLog.objects.values_list('review_id', flat=True)
            )
        return queryset


# ✅ ReviewAdmin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewId', 'product_name', 'convenient_store', 'review_content', 'sentiment_analysis_taste','sentiment_analysis_cost', 'keyword_evaluation', 'created_at')
    list_filter = (ConvenientStoreFilter, SentimentFilter, KeywordFilter)
    search_fields = ('product__product_name', 'tasteContent', 'priceContent', 'convenienceContent')
    ordering = ('-created_at',)
    actions = [analyze_selected_reviews_sentiment, analyze_selected_reviews_keyword]

    def product_name(self, obj):
        return obj.product.product_name if obj.product else "-"
    product_name.short_description = "상품명"

    def convenient_store(self, obj):
        return obj.product.convenient_store_name if obj.product else "-"
    convenient_store.short_description = "편의점"

    def review_content(self, obj):
        content_dict = {
            "맛": obj.tasteContent if obj.tasteContent else "-",
            "가격": obj.priceContent if obj.priceContent else "-",
            "특징": obj.convenienceContent if obj.convenienceContent else "-"
        }

        # Dict 형태의 내용을 줄바꿈 적용하여 표시
        content_html = "<br>".join([f'<strong>{key}:</strong> {value}' for key, value in content_dict.items()])

        return mark_safe(content_html)

    review_content.short_description = "리뷰 내용"

    def sentiment_analysis_taste(self, obj):
        taste_pos_count, taste_neg_count = 0, 0

        taste_logs = TasteLog.objects.filter(review=obj)

        if not taste_logs:
            return format_html('<span style="color:gray;">평가전</span>')

        for taste_log in taste_logs:
            if taste_log.PosNeg == 2:
                taste_pos_count += 1
            elif taste_log.PosNeg == 0:
                taste_neg_count += 1

        return mark_safe(f'<span style="color:green;">긍정: {taste_pos_count}</span><br>'
                     f'<span style="color:red;">부정: {taste_neg_count}</span>')

    sentiment_analysis_taste.short_description = "맛 평가"

    def sentiment_analysis_cost(self, obj):
        price_pos_count, price_neg_count = 0, 0

        price_logs = PriceLog.objects.filter(review=obj)

        if not price_logs:
            return format_html('<span style="color:gray;">평가전</span>')

        for taste_log in price_logs:
            if taste_log.PosNeg == 2:
                price_pos_count += 1
            elif taste_log.PosNeg == 0:
                price_neg_count += 1

        return mark_safe(f'<span style="color:green;">긍정: {price_pos_count}</span><br>'
                     f'<span style="color:red;">부정: {price_neg_count}</span>')

    sentiment_analysis_cost.short_description = "가격 평가"

    def sentiment_analysis_taste(self, obj):
        """맛 평가 감성 분석을 Dict 형태로 변환하고 줄바꿈 적용"""
        taste_pos_count = TasteLog.objects.filter(review=obj, PosNeg=2).count()
        taste_neg_count = TasteLog.objects.filter(review=obj, PosNeg=0).count()

        taste_dict = {
            "긍정": taste_pos_count,
            "부정": taste_neg_count
        }

        # Dict 형태의 내용을 줄바꿈 적용하여 표시
        taste_html = "<br>".join([f'<strong>{key}:</strong> {value}' for key, value in taste_dict.items()])

        return mark_safe(taste_html)  # ✅ HTML 적용하여 Admin에서 줄바꿈 표시

    sentiment_analysis_taste.short_description = "맛 평가"

    def sentiment_analysis_cost(self, obj):
        """가격 평가 감성 분석을 Dict 형태로 변환하고 줄바꿈 적용"""
        price_pos_count = PriceLog.objects.filter(review=obj, PosNeg=1).count()
        price_neg_count = PriceLog.objects.filter(review=obj, PosNeg=0).count()

        price_dict = {
            "긍정": price_pos_count,
            "부정": price_neg_count
        }

        # Dict 형태의 내용을 줄바꿈 적용하여 표시
        price_html = "<br>".join([f'<strong>{key}:</strong> {value}' for key, value in price_dict.items()])

        return mark_safe(price_html)  # ✅ HTML 적용하여 Admin에서 줄바꿈 표시

    sentiment_analysis_cost.short_description = "가격 평가"

    def keyword_evaluation(self, obj):
        conv_log = ConvenienceLog.objects.filter(review=obj).first()

        if conv_log and conv_log.top_sim_tags and len(conv_log.top_sim_tags) > 1:
            return conv_log.top_sim_tags[0][1]

        return format_html('<span style="color:gray;">평가전</span>')

    keyword_evaluation.short_description = "키워드 평가"