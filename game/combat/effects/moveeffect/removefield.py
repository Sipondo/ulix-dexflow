from .basemoveeffect import BaseMoveEffect


class Removefield(BaseMoveEffect):
    def after_move(self):
        field_effects = self.scene.get_effects_by_type("Field")
        for effect in field_effects:
            self.scene.delete_effect(effect)
        return True
