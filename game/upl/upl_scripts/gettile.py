class GetTile:
    def __init__(self, act, src, user, layerid, x, y):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.layerid = layerid
        self.x = x
        self.y = y
        self.height, self.layer = self.act.game.r_wld.get_layer(layerid)

    def on_read(self):
        return self.layer.get_tile(self.height, self.x, self.y)
