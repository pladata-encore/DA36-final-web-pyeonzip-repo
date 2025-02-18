from abc import ABC, abstractmethod
from review.repository.review_repository import ReviewRepositoryImpl

class ReviewService(ABC):

    @abstractmethod
    def find_by_product_id(self, id):
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
