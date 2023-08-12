from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file("resources/armourui/ui/paneloverview.kv")


class PanelOverview(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, time=None, frame_time=None):
        parent = self.parent.parent
        mon = parent.game.inventory.members[parent.selection_mon]

        self.ids.Name.text = mon.name
        self.ids.Type.text = (
            f"{mon.type1}" if mon.type2 else f"{mon.type1} - {mon.type2}"
        )
        self.ids.Id.text = mon.trainerid

        self.ids.Exp.text = str(mon.current_xp)
        self.ids.Next.text = str(mon.level_xp - mon.current_xp)
        return False
