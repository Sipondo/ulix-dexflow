class Teleport:
    def __init__(self, act, src, user, target_level, target_location, fade=True):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        if user == self.game.m_ent.player:
            self = user
            self.game.m_map.set_level(
                self.game.m_map.convert_mapstring_to_key(target_level)
            )
            position = (self.x, self.y)

            target_location = (int(target_location[0]), int(target_location[1]))

            self.game.r_wld.set_map_via_manager(
                (target_location[0] - position[0], target_location[1] - position[1],),
                fade=fade,
            )
        else:
            self.game.m_ent.delete_entity(user)

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
