from abc import ABC, abstractmethod

from community.entity.models import Community
from community.repository.community_repository import CommunityRepositoryImpl

class CommunityService(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def create_community(self, data, product_ids):
        pass


class CommunityServiceImpl(CommunityService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__community_repository = CommunityRepositoryImpl.get_instance()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_all(self):
        """모든 커뮤니티 게시글 조회"""
        return self.__community_repository.find_all()

    def find_by_id(self, id):
        """ID를 기반으로 특정 커뮤니티 게시글 조회"""
        return self.__community_repository.find_by_id(id)

    def create_community(self, data, product_ids):
        """커뮤니티 게시글 생성 및 저장"""
        community = Community(
            category=data.get("category"),
            author=data.get("author"),
            communityTitle=data.get("communityTitle"),
            communityContent=data.get("communityContent")
        )
        self.__community_repository.save(community)
        self.__community_repository.choose_products(community, product_ids)
        return community
