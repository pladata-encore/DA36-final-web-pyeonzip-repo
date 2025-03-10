from abc import ABC, abstractmethod
from product.entity.models import Product
from review.entity.models import Review
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
    def price_count(self, page_obj):
        pass

    @abstractmethod
    def taste_count(self, page_obj):
        pass

    @abstractmethod
    def conv_keyword(self, product_id):
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
        print(product)
        price_pos_count, price_neg_count = 0, 0
        taste_pos_count, taste_neg_count = 0, 0
        reviews = Review.objects.filter(product_id=product.product_id)
        if len(reviews) >= 10:
            for review in reviews:
                price_pos_count += PriceLog.objects.filter(review_id=review.reviewId, PosNeg=1, Confidence__gte=0.8).count()
                price_neg_count += PriceLog.objects.filter(review_id=review.reviewId, PosNeg=0, Confidence__gte=0.8).count()
                taste_pos_count += TasteLog.objects.filter(review_id=review.reviewId, PosNeg=2, Confidence__gte=0.8).count()
                taste_neg_count += TasteLog.objects.filter(review_id=review.reviewId, PosNeg=0, Confidence__gte=0.8).count()
            try:
                product.price_score = (price_pos_count / (price_pos_count + price_neg_count)) * 100 if (price_pos_count + price_neg_count) > 0 else 50  # NaN 방지
                product.taste_score = (taste_pos_count / (taste_pos_count + taste_neg_count)) * 100 if (taste_pos_count + taste_neg_count) > 0 else 50
            except ZeroDivisionError:
                product.price_score = 50
                product.taste_score = 50
            print(product.price_score, product.taste_score)

        else:
            product.price_score = 50
            product.taste_score = 50

        product.conv_keywords = self.conv_keyword(product_id)
        print(product.conv_keywords)
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

    def price_count(self,page_obj):
        for product in  page_obj:
            pos_count, neg_count = 0, 0
            reviews=Review.objects.filter(product_id=product.product_id)
            for review in reviews:
                pos_count+=PriceLog.objects.filter(review_id=review.reviewId,PosNeg=1).count()
                neg_count+=PriceLog.objects.filter(review_id=review.reviewId,PosNeg=0).count()
            try:
                product.score = (pos_count / pos_count+neg_count) * 100 if pos_count+neg_count > 0 else 50   # NaN 방지
            except:
                product.score=0
            print(product,product.score)
        return page_obj

    def taste_count(self, page_obj):
        pass

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

