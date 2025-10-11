from app.core.models import Item
from app.core.services import item_service
from app.utils import logger, normalize_text
from app.vector.dao import item_vector_dao
from app.vector.domains import ItemVectorDomain


def hierarchical_names(item: Item, max_depth: int = 2) -> list[str]:
    result = [item.name]
    stack = [(item, 0)]

    while stack:
        (current, depth) = stack.pop()
        if depth >= max_depth:
            continue
        for group in current.groups:
            result.append(group.name)
            for modifier in group.items:
                result.append(modifier.name)
                if modifier.groups:
                    stack.append((modifier, depth + 1))

    return result


def build_item_point(item: Item) -> ItemVectorDomain:
    item_name = normalize_text(item.name)

    item_group_modifier_names = ' '.join(hierarchical_names(item))
    all_names = normalize_text(item_group_modifier_names)

    return ItemVectorDomain(id=item.id, name=item_name, full_text=all_names)


def load_data_to_vector_db():
    item_points = [build_item_point(item) for item in item_service.get_by_type('ITEM')]
    item_vector_dao.upsert(item_points)


def main():
    logger.info('vector preprocess start')

    load_data_to_vector_db()

    logger.info('vector preprocessing done')


if __name__ == '__main__':
    main()

__all__ = ['load_data_to_vector_db']
