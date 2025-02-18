from abc import ABC, abstractmethod
from product.repository.product_repository import ProductRepositoryImpl

class ProductService(ABC):
    @abstractmethod
    def find_all(self):
        pass
    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def add_remove_likes(self, product, voter):
        pass

    @abstractmethod
    def find_liker(self, product_id, likes):
        pass
class ProductServiceImpl(ProductService):
    __instance = None

    def __new__(cls):
        print('__new__')
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        print('__init__')
        self.__product_repository = ProductRepositoryImpl.get_instance()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def find_all(self):
        return self.__product_repository.find_all()

    def find_by_id(self,id):
        return self.__product_repository.find_by_id(id)

    def find_liker(self,product_id, likes):
        self.__product_repository.find_liker(product_id, likes)

    def add_remove_likes(self, product_id, likes):
        product = self.__product_repository.find_by_id(product_id)
        liked=self.__product_repository.add_remove_likes(product, likes)
        return product,liked
