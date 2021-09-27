"""function
Task the renderer to redraw given layer.

Tasks the renderer to redraw the layer with given id. SHould be used after making your layer edits via e.g. `Settile()`.

in:
- Numeric: id of the layer to update

"""


class UpdateTiles:
    def __init__(self, act, src, user, layerid):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.layerid = layerid
        height, layer = self.act.game.r_wld.get_layer(layerid)
        layer.update_layer()

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
