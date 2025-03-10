from abc import ABC, abstractmethod
from product.entity.models import Product
from review.entity.models import Review
from django.db.models import Q
from django.db.models import Count
from review.entity.models import PriceLog, TasteLog

class ProductRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass
    @abstractmethod
    def find_by_id(self, id):
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

    def find_by_id(self, id):
        product = Product.objects.get(pk=id)
        price_pos_count, price_neg_count = 0, 0
        taste_pos_count, taste_neg_count = 0, 0
        reviews = Review.objects.filter(product_id=product.product_id)
        for review in reviews:
            price_pos_count += PriceLog.objects.filter(review_id=review.reviewId, PosNeg=1).count()
            price_neg_count += PriceLog.objects.filter(review_id=review.reviewId, PosNeg=0).count()
            taste_pos_count += TasteLog.objects.filter(review_id=review.reviewId, PosNeg=1).count()
            taste_neg_count += TasteLog.objects.filter(review_id=review.reviewId, PosNeg=0).count()
        try:
            product.price_score = (price_pos_count / price_pos_count + price_neg_count) * 100 if price_pos_count + price_neg_count > 0 else 50  # NaN 방지
            product.taste_score = (taste_pos_count / taste_pos_count + taste_neg_count) * 100 if taste_pos_count + taste_neg_count > 0 else 50
        except:
            product.price_score = 0
            product.taste_score = 0
        print(product.price_score, product.taste_score)
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
