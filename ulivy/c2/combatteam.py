from dataclasses import replace, dataclass


@dataclass(frozen=True)
class CombatTeam:
    members = ()

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def copy(self, **changes):
        changes = {**self.__dict__, **changes}
        return replace(self, **changes)
