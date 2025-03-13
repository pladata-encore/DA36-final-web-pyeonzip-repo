from abc import ABC, abstractmethod

from product.entity.models import Product
from review.entity.models import Review, TasteKeywordLog
from django.db.models import Q
from django.db.models import Count
from review.entity.models import PriceLog, TasteLog, ConvenienceLog
import json
from collections import Counter

class ProductRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass
    @abstractmethod
    def find_by_id(self, product_id):
        pass

    @abstractmethod
    def add_remove_likes(self, product, likes):
        pass

    @abstractmethod
    def latest_product(self):
        pass

    @abstractmethod
    def ai_product(self):
        pass

    @abstractmethod
    def ai_score_count(self, products):
        pass

    def ai_score_by_id(self, product_id):
        pass

    @abstractmethod
    def conv_keyword(self, product_id):
        pass

    @abstractmethod
    def taste_keyword(self, product_id):
        pass

class ProductRepositoryImpl(ProductRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_all(self):
        return Product.objects.prefetch_related().order_by('-updated_at')

    def find_by_id(self, product_id):
        product = Product.objects.get(pk=product_id)
        ai_scores = self.ai_score_by_id(product_id)
        product.price_score = ai_scores["price_score"]
        product.taste_score = ai_scores["taste_score"]
        print(product.price_score, product.taste_score)

        product.conv_keywords = self.conv_keyword(product_id)
        print(product.conv_keywords)

        product.taste_pos_keywords = self.taste_keyword(product_id)["positive"]
        print(product.taste_pos_keywords)
        product.taste_neg_keywords = self.taste_keyword(product_id)["negative"]
        print(product.taste_neg_keywords)
        return product

    def add_remove_likes(self, product, likes):
        if product.likes.filter(id=likes.id).exists():
            product.likes.remove(likes)
            return False
        else:
            product.likes.add(likes)
            return True

    def find_by_name(self, query):
        return Product.objects.filter(product_name__icontains=query)


    def latest_product(self):

        # 가장 최근 등록된 상품의 날짜 가져오기
        latest_date = Product.objects.latest("updated_at").updated_at
        latest_products = Product.objects.filter(updated_at=latest_date)

        return latest_products

    def ai_product(self):
        ai_products = Product.objects.annotate(num_reviews=Count('Product_reviews')).filter(num_reviews__gte=10)
        return ai_products

    def ai_score_count(self,products):
        for product in  products:
            price_pos_count, price_neg_count, taste_pos_count, taste_neg_count = 0,0,0,0
            reviews=Review.objects.filter(product_id=product.product_id)
            for review in reviews:
                price_pos_count+=PriceLog.objects.filter(review_id=review.reviewId,PosNeg=1,Confidence__gte=0.6).count()
                price_neg_count+=PriceLog.objects.filter(review_id=review.reviewId,PosNeg=0,Confidence__gte=0.6).count()
                taste_pos_count += TasteLog.objects.filter(review_id=review.reviewId, PosNeg=2, Confidence__gte=0.6).count()
                taste_neg_count += TasteLog.objects.filter(review_id=review.reviewId, PosNeg=0, Confidence__gte=0.6).count()
            try:
                product.price_score = int((price_pos_count / (price_pos_count + price_neg_count)) * 100 if (price_pos_count + price_neg_count) > 0 else 50)
                product.taste_score = int((taste_pos_count / (taste_pos_count + taste_neg_count)) * 100 if (taste_pos_count + taste_neg_count) > 0 else 50)
            except:
                product.price_score=0
                product.taste_score=0
            print("ai",product,product.price_score,product.taste_score)

            product.conv_keywords = self.conv_keyword(product.product_id)[:3]
            print(product.conv_keywords)

        return products


    def ai_score_by_id(self, product_id):
        product = Product.objects.get(pk=product_id)
        price_pos_count, price_neg_count = 0, 0
        taste_pos_count, taste_neg_count = 0, 0
        reviews = Review.objects.filter(product_id=product.product_id)
        if len(reviews) >= 10:
            for review in reviews:
                price_pos_count += PriceLog.objects.filter(review_id=review.reviewId, PosNeg=1, Confidence__gte=0.6).count()
                price_neg_count += PriceLog.objects.filter(review_id=review.reviewId, PosNeg=0, Confidence__gte=0.6).count()
                taste_pos_count += TasteLog.objects.filter(review_id=review.reviewId, PosNeg=2, Confidence__gte=0.6).count()
                taste_neg_count += TasteLog.objects.filter(review_id=review.reviewId, PosNeg=0,Confidence__gte=0.6).count()
            try:
                price_score = int((price_pos_count / (price_pos_count + price_neg_count)) * 100) if (price_pos_count + price_neg_count) > 0 else 50  # NaN 방지
                taste_score = int((taste_pos_count / (taste_pos_count + taste_neg_count)) * 100) if (taste_pos_count + taste_neg_count) > 0 else 50
            except ZeroDivisionError:
                price_score = 0
                taste_score = 0
        else:
            price_score = 50
            taste_score = 50

        return {"price_score": price_score, "taste_score": taste_score}

    def conv_keyword(self, product_id):
        """
        특정 product_id의 리뷰들을 기반으로 태그 빈도수를 계산하여
        상위 5개를 product.conv_keywords에 저장
        """
        reviews = Review.objects.filter(product_id=product_id)

        all_tags = []
        # 편의성 로그 조회 및 태그 추출
        for review in reviews:
            convenience_logs = ConvenienceLog.objects.filter(review_id=review.reviewId)
            for log in convenience_logs:
                try:
                    top_sim_tags = log.top_sim_tags # 리스트 형태로 저장되어 있음
                    all_tags.extend([tag[1] for tag in sorted(top_sim_tags, key=lambda x: x[2], reverse=True)[:5]])
                except json.JSONDecodeError:
                    continue  # JSON 오류 무시하고 진행

        # 태그 빈도수 계산
        tag_counts = Counter(all_tags)

        # 빈도수 높은 상위 5개 태그 추출 @TODO min 빈도수 계산 필요
        top_5_tags = [tag for tag, _ in tag_counts.most_common(5)]

        return top_5_tags

    def taste_keyword(self, product_id):
        """
        특정 product_id의 리뷰들을 기반으로 태그 빈도수를 계산하여
        긍정, 부정 각각 상위 3개를 product.taste_keywords에 저장
        """
        reviews = Review.objects.filter(product_id=product_id)

        all_pos_tags = []
        all_neg_tags = []

        # 리뷰를 조회하여 문장별 감성 분석 결과와 키워드 추출
        for review in reviews:
            taste_logs = TasteLog.objects.filter(review_id=review.reviewId)
            taste_keyword_logs = TasteKeywordLog.objects.filter(review_id=review.reviewId)

            pos_sentences = set()
            neg_sentences = set()

            # 감성 분석 결과를 바탕으로 긍정/부정 문장 분류
            for log in taste_logs:
                if log.PosNeg == 2:
                    pos_sentences.add(log.sentence_id)  # 문장 ID 사용
                elif log.PosNeg == 0:
                    neg_sentences.add(log.sentence_id)

            # 키워드 추출 및 긍/부정 문장별로 분류
            for log in taste_keyword_logs:
                try:
                    top_sim_tags = log.top_sim_tags  # 리스트 형태로 저장됨
                    sorted_tags = [tag[1] for tag in sorted(top_sim_tags, key=lambda x: x[2], reverse=True)[:5]]

                    if log.sentence_id in pos_sentences:
                        all_pos_tags.extend(sorted_tags)
                    elif log.sentence_id in neg_sentences:
                        all_neg_tags.extend(sorted_tags)
                except json.JSONDecodeError:
                    continue  # JSON 오류 무시하고 진행

        # 태그 빈도수 계산
        pos_tag_counts = Counter(all_pos_tags)
        neg_tag_counts = Counter(all_neg_tags)

        # 빈도수 높은 상위 3개 태그 추출
        top_3_pos_tags = [tag for tag, _ in pos_tag_counts.most_common(3)]
        top_3_neg_tags = [tag for tag, _ in neg_tag_counts.most_common(3)]

        return {"positive": top_3_pos_tags, "negative": top_3_neg_tags}


