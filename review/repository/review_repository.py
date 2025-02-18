from abc import ABC, abstractmethod
from review.entity.models import Review
from django.db.models import Q

class ReviewRepository(ABC):

    @abstractmethod
    def find_by_product_id(self, product_id):
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
        return Review.objects.filter(productId_id=product_id)

