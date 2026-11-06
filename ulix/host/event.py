from dataclasses import dataclass
from typing import Literal

EventKind = Literal['key_down', 'key_up', 'pointer_down', 'pointer_up', 'pointer_move']


@dataclass(frozen=True)
class Event:
    kind: EventKind
    key: str = ''
    x: float = 0.0
    y: float = 0.0
    pointer: int = 0
