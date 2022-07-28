from ..baseui import BaseUI
from kivy.lang import Builder

Builder.load_file("ulivy/interface/modernui/uicinematic.kv")


class UICinematic(BaseUI):
    def on_enter(self, **kwargs):
        self.selection = 0
        self.lock = False
        self.block_input = False

    def update(self, time=None, frame_time=None):
        self.ids.DialogueText.text = self.gstate.dialogue or ""

        if self.gstate.dialogue:
            self.gstate.dialogue = self.clean_dialogue(self.gstate.dialogue)
            self.ids.DialogueWindow.opacity = 1
        else:
            self.ids.DialogueWindow.opacity = 0
        self.set_choice_window(self.gstate.options)
        self.highlight_selection()
        return False

    def event_keypress(self, key, modifiers):
        if self.lock == False:
            if key == "down":
                if self.gstate.options:
                    self.selection = (self.selection + 1) % self.max_selection
                    self.game.r_aud.effect("select")
            elif key == "up":
                if self.gstate.options:
                    self.selection = (self.selection - 1) % self.max_selection
                    self.game.r_aud.effect("select")
            elif key == "interact":
                if self.gstate.options:
                    print(
                        "Selected: ", self.gstate.options[self.selection],
                    )
                    self.game.selection = self.selection
                    self.game.selection_text = self.gstate.options[self.selection]
                    self.game.r_aud.effect("confirm")
                else:
                    self.game.r_aud.effect("select")
                self.gstate.options = []
                self.selection = 0
                self.gstate.dialogue = None
                self.gstate.author = None
                self.gstate.spr_talker = None
        self.highlight_selection()

    def set_choice_window(self, options):
        l = len(options)

        self.ids.ChoiceWindow_1.opacity = 1 if l > 0 else 0
        self.ids.ChoiceWindow_2.opacity = 1 if l > 1 else 0
        self.ids.ChoiceWindow_3.opacity = 1 if l > 2 else 0
        self.ids.ChoiceWindow_4.opacity = 1 if l > 3 else 0

        if l > 0:
            self.ids.ChoiceText_1.text = options[0]
        if l > 1:
            self.ids.ChoiceText_2.text = options[1]
        if l > 2:
            self.ids.ChoiceText_3.text = options[2]
        if l > 3:
            self.ids.ChoiceText_4.text = options[3]

    def highlight_selection(self):
        s = self.selection
        self.ids.ChoiceBackground_1.source = (
            f'ulivy/interface/modernui/dialogue_choice{"_high" if s==0 else ""}.png'
        )
        self.ids.ChoiceBackground_2.source = (
            f'ulivy/interface/modernui/dialogue_choice{"_high" if s==1 else ""}.png'
        )
        self.ids.ChoiceBackground_3.source = (
            f'ulivy/interface/modernui/dialogue_choice{"_high" if s==2 else ""}.png'
        )
        self.ids.ChoiceBackground_4.source = (
            f'ulivy/interface/modernui/dialogue_choice{"_high" if s==3 else ""}.png'
        )

    def clean_dialogue(self, dialogue):
        return (
            dialogue.replace("{player.name}", self.game.m_ent.player.name)
            .replace("{player.he}", self.game.m_ent.player.he)
            .replace("{player.his}", self.game.m_ent.player.his)
            .replace("{player.che}", self.game.m_ent.player.che)
            .replace("{player.chis}", self.game.m_ent.player.chis)
        )

    def draw_interface(self, time, frame_time):
        return

        if self.spr_talker:
            self.game.r_int.draw_image(
                self.spr_talker, (0.8, 0.7), centre=True, size=3, safe=True
            )

        # self.game.r_int.draw_rectangle((0.024, 0.83), to=(0.984, 0.99), col="grey")

        if self.author is not None and self.author:
            self.game.r_int.draw_image(
                "namebox", (0.02, 0.75),
            )
            self.game.r_int.draw_text(
                self.author, (0.025, 0.755), to=(0.30, 0.80), bcol=None,
            )

        if self.dialogue:
            self.game.r_int.draw_image(
                "textbox", (0.02, 0.82),
            )
            self.game.r_int.draw_text(
                self.dialogue if self.dialogue is not None else "",
                (0.025, 0.825),
                to=(0.98, 0.98),
                bcol=None,
            )

        if self.options:
            self.game.r_int.draw_rectangle(
                (0.75, 0.3), size=(0.15, 0.04 + 0.1 * len(self.options)), col="black"
            )
            for i, name in enumerate(self.options):
                self.game.r_int.draw_text(
                    f"{self.selection == i and '' or ''}{name}",
                    (0.76, 0.31 + 0.08 * i),
                    size=(0.13, 0.06),
                    centre=False,
                    bcol=self.selection == i and "yellow" or "white",
                )

    @property
    def max_selection(self):
        return len(self.gstate.options)
