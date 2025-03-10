from abc import ABC, abstractmethod
from product.repository.product_repository import ProductRepositoryImpl

class ProductService(ABC):
    @abstractmethod
    def find_all(self):
        pass
    @abstractmethod
    def find_by_id(self, product_id):
        pass

    @abstractmethod
    def add_remove_likes(self, product, voter):
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

    def find_by_id(self,product_id):
        return self.__product_repository.find_by_id(product_id)


    def add_remove_likes(self, product_id, likes):
        product = self.__product_repository.find_by_id(product_id)
        liked=self.__product_repository.add_remove_likes(product, likes)
        return product,liked

    def find_by_name(self, query):
        return self.__product_repository.find_by_name(query)

    def latest_product(self):
        return self.__product_repository.latest_product()

    def ai_product(self):
        return self.__product_repository.ai_product()

    def price_count(self, page_obj):
         return self.__product_repository.price_count(page_obj)