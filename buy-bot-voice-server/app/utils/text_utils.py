def normalize_text(text: str) -> str:
    return text.strip().lower() if text else ''


__all__ = ['normalize_text']
