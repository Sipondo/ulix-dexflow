"""function
Teleports the user to the specified location in a different map.

Teleports the user to the specified location in a different map. This function should be used in all custom actions that require map travel.

in:
- String: level to teleport to
- Tuple of numeric of length 2: position to teleport to
- [Optional, False] Bool: whether to fade to the target map

"""


class Teleport:
    def __init__(self, act, src, user, target_level, target_location, fade=False):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game
        fade = False

        if user == self.game.m_ent.player:
            self = user
            self.game.m_map.set_level(
                self.game.m_map.convert_mapstring_to_key(target_level)
            )
            self.game.m_ent.player.game_position = (
                int(target_location[0]),
                int(target_location[1]),
            )
            self.game.r_til.offset = (0.5, 13 / 16)
            self.game.m_col.offset = (0.5, 13 / 16)
            self.game.r_til.set_map_via_manager(  # TODO: this shouldn't be called directly
                (0, 0,), fade=False,
            )
        else:
            self.game.m_ent.delete_entity(user)

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
