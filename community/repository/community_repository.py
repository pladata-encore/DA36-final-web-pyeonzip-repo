from abc import abstractmethod, ABC

from community.entity.models import Community
from product.entity.models import Product


class CommunityRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def find_by_user_id(self, user_id):
        pass

    @abstractmethod
    def save(self, community):
        pass

    @abstractmethod
    def choose_products(self, community, product_ids):
        pass

class CommunityRepositoryImpl(CommunityRepository):
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
        return Community.objects.select_related("category").prefetch_related("products").all()

    def find_by_id(self, id):
        return Community.objects.prefetch_related("products").get(pk=id)

    def find_by_user_id(self, user_id):
        return Community.objects.filter(author_id=user_id).select_related('author')

    def save(self, community):
        community.save()

    def choose_products(self, community, product_ids):
        products = Product.objects.filter(product_id__in=product_ids)
        community.products.set(products)
