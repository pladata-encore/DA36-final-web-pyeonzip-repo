from abc import ABC, abstractmethod
from django.utils.timezone import now

from community.entity.models import Community
from community.repository.community_repository import CommunityRepositoryImpl

class CommunityService(ABC):
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
    def create_community(self, data, product_ids, author):
        pass

    def add_vote(self, community_id, user):
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

    def find_by_id(self, community_id):
        """ID를 기반으로 특정 커뮤니티 게시글 조회"""
        return self.__community_repository.find_by_id(community_id)

    def find_by_user_id(self, user_id):
        return self.__community_repository.find_by_user_id(user_id)

    def create_community(self, data, product_ids, author):
        """커뮤니티 게시글 생성 및 저장"""
        community = Community(
            category=data.get("category"),
            author=author,
            communityTitle=data.get("communityTitle"),
            communityContent=data.get("communityContent")
        )
        self.__community_repository.save(community)
        self.__community_repository.choose_products(community, product_ids)
        return community

    def add_vote(self, community_id, user):
        community = self.__community_repository.find_by_id(community_id)

        if community.deadline < now().date():
            return False  # 투표 기간이 종료된 경우 False 반환

        return self.__community_repository.add_vote(community, user)
