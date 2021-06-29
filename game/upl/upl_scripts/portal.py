def portal(self, target_level, target_location, fade):
    self.game.m_map.set_level(self.game.m_map.convert_mapstring_to_key(target_level))
    position = (self.x, self.y)

    direc = self.game.m_ent.player.get_dir()

    print(target_location, position, direc)

    self.game.r_wld.set_map_via_manager(
        (
            target_location[0] - position[0] + direc[0],
            target_location[1] - position[1] + direc[1],
        ),
        fade=fade,
    )
