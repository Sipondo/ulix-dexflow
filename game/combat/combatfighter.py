import numbers


class CombatFighter:
    def __init__(self, game, fighter):
        self.game = game

        if isinstance(fighter, numbers.Number):
            fighter = self.game.m_pbs.get_fighter(fighter)

        self.name = str(fighter["name"])
        self.id = fighter.name
        self.hp = 350

        self.starting_hp = fighter.current_hp

        self.sprite = self.game.m_res.prepare_battle_animset(f"{str(self.id).zfill(3)}")
