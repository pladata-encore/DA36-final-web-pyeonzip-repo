from abc import ABC, abstractmethod
from review.entity.models import Review
from users.entity.models import UserDetail
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
    def review_recommenders(self, review,recommender):
        pass

    @abstractmethod
    def create(self, form):
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
        return Review.objects.get(reviewId=review_id)

    def review_recommenders(self, review, recommender):

        if review.recommender.filter(id=recommender.id).exists():
            review.recommender.remove(recommender)
            return False
        else:
            review.recommender.add(recommender)
            return True

    def create(self, form):
        form.save()
        return form


