class Portal:
    def __init__(self, act, user, target_level, target_location, fade):
        act.funcs.append(self)
        self = user
        print(self.target)
        self.game.m_map.set_level(
            self.game.m_map.convert_mapstring_to_key(target_level)
        )
        position = (self.x, self.y)

        direc = self.game.m_ent.player.get_dir()

        self.game.r_wld.set_map_via_manager(
            (
                target_location[0] - position[0] + direc[0],
                target_location[1] - position[1] + direc[1],
            ),
            fade=fade,
        )

    def on_tick(self, time=None, frame_time=None):
        return True
