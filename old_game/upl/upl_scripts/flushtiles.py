"""function
Revert all tiles in the given layer to transparent.

Set all tiles in the given layer to transparent, effectively starting over with a clean slate.

in:
- Numeric: id of the layer to flush

"""


class FlushTiles:
    def __init__(self, act, src, user, layerid):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.layerid = layerid
        height, layer = self.act.game.r_wld.get_layer(layerid)
        layer.flush_tiles(height)

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
