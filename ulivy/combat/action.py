import enum
import dataclasses
import typing


class ActionType(enum.Enum):
    ATTACK = enum.auto()
    SWITCH = enum.auto()
    RUN = enum.auto()
    SENDOUT = enum.auto()
    ITEM = enum.auto()
    CATCH = enum.auto()
    FORGET_MOVE = enum.auto()
    # NOTHING = enum.auto()


@dataclasses.dataclass
class Action:
    a_type: ActionType
    a_index: typing.Optional[int] = None
    a_data: typing.Optional = None
    user: typing.Optional[tuple] = None
    target: typing.Optional[tuple] = None
    priority: typing.Optional[int] = 6
