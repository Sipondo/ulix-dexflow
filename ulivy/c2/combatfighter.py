from dataclasses import replace, dataclass


@dataclass(frozen=True)
class CombatFighter:
    data = None
    type1 = None
    type2 = None
    level = 1
    gender = "Genderless"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def copy(self, **changes):
        return replace(self, **changes)
