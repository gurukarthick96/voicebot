import uuid

from num2words import num2words


def normalize_text(text: str) -> str:
    return text.strip().lower() if text else ''


def number_to_text(number) -> str:
    return num2words(number)


def text_to_uuid(text: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, text))


__all__ = ['normalize_text', 'number_to_text', 'text_to_uuid']
