from app.core.models import Item, Group
from app.core.samples import load_menu_data, print_menu_data

sample_items, sample_groups = load_menu_data('app/core/samples/menu_data.json')
print_menu_data(sample_items)

items = [Item.from_dict(item) for item in sample_items]
groups = [Group.from_dict(group) for group in sample_groups]

__all__ = ['items', 'groups']
