from abc import ABC, abstractmethod
from review.entity.models import Review
from django.db.models import Q

class ReviewRepository(ABC):

    @abstractmethod
    def find_by_product_id(self, product_id):
        pass

    @abstractmethod
    def find_by_user_id(self, user_id):
        pass

    @abstractmethod
    def delete(self, review_id):
        pass

    @abstractmethod
    def find_by_review_id(self, review_id):
        pass

    @abstractmethod
    def review_recommenders(self, review_id):
        pass

class ReviewRepositoryImpl(ReviewRepository):
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

    def find_by_product_id(self, product_id):
        return Review.objects.filter(product_id=product_id)

    def find_by_user_id(self, user_id):
        return Review.objects.filter(author=user_id).prefetch_related('product')

    def delete(self, review_id):
        review = Review.objects.get(reviewId=review_id)
        review.delete()
        return review

    def find_by_review_id(self,review_id):
        return Review.objects.get(review_id=review_id)

    def review_recommenders(self, review, recommenders):
        if review.recommenders.filter(id=recommenders.id).exists():
            review.recommenders.remove(recommenders)
        else:
            review.recommenders.add(recommenders)
            return True
