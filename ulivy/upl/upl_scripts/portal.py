"""function
Portals the user to the specified location in a different map.

Portals the user to the specified location in a different map. Closely connected to the **portal** region and should in general not be used in other situations.

in:
- String: level to portal to
- Tuple of numeric of length 2: position to portal to
- [Optional, True] Bool: whether to fade to the target map

"""


class Portal:
    def __init__(self, act, src, user, target_level, target_location, fade=True):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        if user == self.game.m_ent.player:
            self = src
            self.game.m_map.set_level(
                self.game.m_map.convert_mapstring_to_key(target_level)
            )
            position = (self.x, self.y)

            direc = user.get_dir()

            target_location = (int(target_location[0]), int(target_location[1]))

            self.game.r_fbo.r_til.set_map_via_manager(  # TODO: this shouldn't be called directly
                (
                    target_location[0] - position[0] + direc[0],
                    target_location[1] - position[1] + direc[1],
                ),
                fade=fade,
            )
        else:
            self.game.m_ent.delete_entity(user)

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
