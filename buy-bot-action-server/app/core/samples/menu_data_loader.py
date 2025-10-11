import json
from typing import Any


def load_menu_data(json_file_path: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    sample_groups = []
    sample_items = []

    for group_data in data['groups']:
        group = {
            'id': group_data['id'],
            'name': group_data['name'],
            'items': []
        }
        sample_groups.append(group)

    for item_data in data['items']:
        item = {
            'id': item_data['id'],
            'name': item_data['name'],
            'type': item_data['type'],
            'price': item_data['price'],
            'groups': []
        }
        sample_items.append(item)

    group_map = {group['id']: group for group in sample_groups}
    item_map = {item['id']: item for item in sample_items}

    for group_data in data['groups']:
        group = group_map[group_data['id']]
        for item_id in group_data['item_ids']:
            if item_id in item_map:
                group['items'].append(item_map[item_id])

    for item_data in data['items']:
        item = item_map[item_data['id']]
        for group_id in item_data['group_ids']:
            if group_id in group_map:
                item['groups'].append(group_map[group_id])

    return sample_items, sample_groups


def print_menu_data(sample_items: list[dict[str, Any]]):
    print('loaded menu items:')
    for item in sample_items:
        if item['type'] == 'ITEM':
            print(f"• {item['name']} - ${item['price']:.2f}")
            if item['groups']:
                for group in item['groups']:
                    print(f"  └─ {group['name']}: {', '.join([i['name'] for i in group['items']])}")


__all__ = ['load_menu_data', 'print_menu_data']
