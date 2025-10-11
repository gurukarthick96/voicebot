from __future__ import annotations

from app.core.data import items, groups
from app.core.models import Item, Group
from app.utils import find_first_by_predicate, find_all_by_predicate, singleton


@singleton
class ItemService:

    def __init__(self):
        self.items: list[Item] = items

    def get_all(self) -> list[Item]:
        return self.items

    def get_by_type(self, item_type: str) -> list[Item]:
        return find_all_by_predicate(self.items, lambda item: item.type == item_type)

    def get_by_id(self, item_id: str) -> Item:
        return find_first_by_predicate(self.items, lambda item: item.id == item_id)


item_service = ItemService()


@singleton
class GroupService:

    def __init__(self):
        self.groups: list[Group] = groups

    def get_all(self) -> list[Group]:
        return self.groups

    def get_by_id(self, group_id: str) -> Group:
        return find_first_by_predicate(self.groups, lambda group: group.id == group_id)


group_service = GroupService()

__all__ = ['ItemService', 'item_service', 'GroupService', 'group_service']
