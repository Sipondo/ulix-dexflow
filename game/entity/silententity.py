from .baseentity import BaseEntity


class SilentEntity(BaseEntity):
    def on_interact(self):
        pass

    def on_render(self):
        pass

    def on_enter(self):
        pass
