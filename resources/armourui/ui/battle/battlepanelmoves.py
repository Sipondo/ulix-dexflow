from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file("resources/armourui/ui/battle/battlepanelmoves.kv")


# class TypeMarker(RelativeLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)


# class MoveCell(RelativeLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)


class BattlePanelMoves(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, time=None, frame_time=None):
        parent = self.parent.parent
        mon = parent.game.inventory.members[0]  # TODO: update

        for i, cell in enumerate(
            (self.ids.Move1, self.ids.Move2, self.ids.Move3, self.ids.Move4)
        ):
            if i >= len(mon.actions):
                cell.opacity = 0.0
                continue
            cell.opacity = 1.0
            move = mon.actions[i]

            cell.ids.Name.text = move.name
            cell.ids.Type.ids.Type.source = f"resources/armourui/graphics/interface/general/typemarker/{move.type.lower()}.png"
            cell.ids.Type.ids.Name.text = move.type.upper()

        return False

    def event_keypress(self, key, modifiers):
        pass
