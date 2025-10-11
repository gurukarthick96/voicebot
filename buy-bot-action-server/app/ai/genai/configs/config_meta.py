from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ConfigMeta:
    system_instruction: Optional[str]
    response_mime_type: Optional[str]
    response_schema: Optional[type[any]]


__all__ = ['ConfigMeta']
