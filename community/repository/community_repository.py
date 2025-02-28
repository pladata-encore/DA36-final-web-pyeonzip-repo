from abc import abstractmethod, ABC
from django.db.models import Count
from django.utils.timezone import now

from community.entity.models import Community
from product.entity.models import Product


class CommunityRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, community_id):
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

    @abstractmethod
    def add_vote(self, community, user):
        pass

    @abstractmethod
    def find_unvoted_communities(self, user):
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

        return Community.objects.select_related("category")\
            .prefetch_related("products")\
            .annotate(vote_count=Count("voter"))\
            .order_by('-created_at')

    def find_by_id(self, community_id):
        return Community.objects.prefetch_related("products").get(pk=community_id)

    def find_by_user_id(self, user_id):
        return Community.objects.filter(author_id=user_id).select_related('author')

    def save(self, community):
        community.save()

    def choose_products(self, community, product_ids):
        products = Product.objects.filter(product_id__in=product_ids)
        community.products.set(products)

    def add_vote(self, community, user):
        return community.add_vote(user) # ✅ 중간 테이블에 직접 추가

    def find_unvoted_communities(self, user):
        return Community.objects.exclude(voter=user).filter(deadline__gte=now().date())
