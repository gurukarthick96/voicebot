import json
from typing import Any


def json_to_dict(json_text: str) -> dict[str, Any]:
    try:
        return json.loads(json_text)
    except (TypeError, json.JSONDecodeError):
        raise ValueError(f'invalid or missing JSON: {json_text}')


__all__ = ['json_to_dict']
