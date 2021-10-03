import numbers


class CombatFighter:
    def __init__(self, game, scene, fighter):
        self.game = game
        self.scene = scene

        if isinstance(fighter, str):
            fighter = self.game.m_pbs.get_fighter_by_name(fighter)
        elif isinstance(fighter, numbers.Number):
            fighter = self.game.m_pbs.get_fighter(fighter)

        self.name = str(fighter["name"])
        self.id = fighter.name

        # self.starting_hp = fighter.current_hp

        self.data = fighter.copy()
        self.actions = []
        self.sprite = self.game.m_res.prepare_battle_animset(f"{str(self.id).zfill(3)}")

    @property
    def series(self):
        return self.data
