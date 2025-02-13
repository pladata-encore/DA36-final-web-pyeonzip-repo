from abc import ABC, abstractmethod
from product.repository.product_repository import ProductRepositoryImpl

class ProductService(ABC):
    @abstractmethod
    def find_all(self):
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
