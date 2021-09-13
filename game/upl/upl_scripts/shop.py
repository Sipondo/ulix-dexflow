class Shop:
    def __init__(self, act, src, user, obj):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.obj = obj
        self.src = src
        self.user = user
        self.options = self.user.options
        # self.items = [
        #     isinstance(x, tuple)
        #     and self.act.game.inventory.get_item(x[0])
        #     or self.act.game.inventory.get_item(x)
        #     for x in self.options
        # ]
        #
        # for item, opt in zip(self.items, self.options):
        #     if isinstance(opt, tuple) and len(opt) > 1:
        #         item.price = int(opt[1])

        self.act.game.m_gst.switch_state("shop", self.options, self.user)

        self.act.game.m_gst.current_state.dialogue = self.obj
        self.act.game.m_gst.current_state.author = (
            "" if self.user == self.act.game else self.user.name
        )
        # self.act.game.m_gst.current_state.shop = self.obj

        # self.act.game.m_gst.current_state.options = self.items

    def on_tick(self, time=None, frame_time=None):
        if self.act.game.m_gst.current_state.dialogue is not None:
            return False
        return True

    def on_read(self):
        return None
