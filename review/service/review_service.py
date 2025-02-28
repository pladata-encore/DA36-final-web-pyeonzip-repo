from abc import ABC, abstractmethod

from review.entity.models import Review
from review.repository.review_repository import ReviewRepositoryImpl

class ReviewService(ABC):

    @abstractmethod
    def find_by_product_id(self, id):
        pass

    @abstractmethod
    def find_by_user_id(self, user_id):
        pass

    @abstractmethod
    def find_by_review_id(self, review_id):
        pass

    @abstractmethod
    def add_remove_recommend(self, review_id,recommenders):
        pass
    @abstractmethod
    def create(self,review):
        pass

    @abstractmethod
    def user_detail_id(self, user_id):
        pass

class ReviewServiceImpl(ReviewService):
    __instance = None

    def __new__(cls):
        print('__new__')
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        print('__init__')
        self.__review_repository = ReviewRepositoryImpl.get_instance()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_by_product_id(self,product_id):
        return self.__review_repository.find_by_product_id(product_id)

    def find_by_user_id(self, user_id):
        return self.__review_repository.find_by_user_id(user_id)

    def delete(self, review_id):
        self.__review_repository.delete(review_id)

    def find_by_review_id(self, review_id):
        return self.__review_repository.find_by_review_id(review_id)

    def add_remove_recommend(self, review_id, recommenders):
        review = self.__review_repository.find_by_review_id(review_id)
        recommended = self.__review_repository.review_recommenders(review, recommenders)
        return review, recommended

    def create(self,review):
        return self.__review_repository.create(review)

    def user_detail_id(self, user_id):
        return self.__review_repository.user_detail_id(user_id)