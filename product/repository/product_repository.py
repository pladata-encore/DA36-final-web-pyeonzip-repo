from abc import ABC, abstractmethod
from product.entity.models import Product
from django.db.models import Q

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
        return Product.objects.get(pk=id)

    def add_remove_likes(self, product, likes):
        if product.likes.filter(id=likes.id).exists():
            product.likes.remove(likes)
            return False
        else:
            product.likes.add(likes)
            return True
