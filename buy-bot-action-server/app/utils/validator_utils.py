def validate_required_dict_fields(data: dict, required_fields: list[str], allow_empty: bool = False) -> None:
    for field_path in required_fields:
        keys = field_path.split('.')
        value = data

        for key in keys:
            if not isinstance(value, dict) or key not in value:
                raise ValueError(f'missing required field: {field_path}')
            value = value[key]

        if allow_empty or value in [None, '', [], {}]:
            raise ValueError(f'empty or invalid required field: {field_path}')


__all__ = ['validate_required_dict_fields']
