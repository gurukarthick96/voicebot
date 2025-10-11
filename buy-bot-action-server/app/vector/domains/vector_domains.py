from __future__ import annotations

from pydantic import BaseModel


class ItemVectorDomain(BaseModel):
    id: str
    name: str
    full_text: str

    @classmethod
    def from_dict(cls, item_dict: dict) -> ItemVectorDomain:
        return cls(**item_dict)


__all__ = ['ItemVectorDomain']
