from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file("resources/armourui/ui/panelmoves.kv")


class TypeMarker(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MoveCell(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PanelMoves(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, time=None, frame_time=None):
        parent = self.parent.parent
        mon = parent.game.inventory.members[parent.selection_mon]

        return False
