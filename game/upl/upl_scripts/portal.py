def portal(self, target_level, target_location, target_direction, fade):
    self.game.m_map.set_level(target_level)

    # direc = self.game.m_ent.player.get_dir()
    # locat = self.location[0]
    # self.game.r_wld.set_map_via_manager(
    #     (
    #         self.entity.target_location[0] - locat[0] + direc[0],
    #         self.entity.target_location[1] - locat[1] + direc[1],
    #     ),
    #     fade=fade,
    # )
