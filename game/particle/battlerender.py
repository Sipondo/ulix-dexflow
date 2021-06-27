from game.particle.battlemovement import BattleMovement
import numpy as np
from array import array

import moderngl
from moderngl_window import geometry

from .battlemovement import BattleMovement


class BattleRender:
    def __init__(self, game):
        self.ctx = game.ctx
        self.game = game

        self.bmove = BattleMovement(game, self)

        self.poke1_set = None
        self.poke2_set = None

        self.prog = self.game.m_res.get_program("flattened_battle_entity")
        self.prog["Texture"] = 0
        self.prog_bg = self.game.m_res.get_program("battle_parallax")

        self.dark = 1.0
        self.dark_to = None
        self.dark_speed = 1.0
        self.dark_recover = True
        self.dark_direction = 1

        self.battle_shake = 1.0
        self.prog_bg["Brightness"] = self.dark
        self.camera = self.game.m_cam

        self.brightness = [1.0, 1.0]
        self.prog["Brightness"] = 1.0
        self.prog["Size"].value = 5.0

        self.character_offset = 20

        self.vbo_pkm = self.ctx.buffer(array("f", [0.0, 0.0, 0.0]))
        self.vao_pkm = self.ctx.vertex_array(
            self.prog, [(self.vbo_pkm, "3f", "in_pos")],
        )

        self.environment = self.game.m_res.get_environment("forest")

        # self.tex_p_cls = self.game.m_res.get_texture("splash", "parallax_close_shift_d")
        # self.tex_p_far = self.game.m_res.get_texture("splash", "parallax_far_shift_d")

        # Rendering
        self.render_prog = self.game.m_res.get_program("texture")
        self.render_prog["texture0"].value = 0
        self.quad_fs = geometry.quad_fs()

        # RGBA color/diffuse layer for alpha
        self.alpha_diffuse = self.ctx.texture(self.game.resolution_combat_particles, 4)
        self.alpha_diffuse.filter = moderngl.NEAREST, moderngl.NEAREST

        # RGBA color/diffuse layer for solid
        self.solid_diffuse = self.ctx.texture(self.game.resolution_combat_particles, 4)
        self.solid_diffuse.filter = moderngl.NEAREST, moderngl.NEAREST

        # Textures for storing depth values
        self.alpha_depth = self.ctx.depth_texture(self.game.resolution_combat_particles)
        # self.solid_depth = self.ctx.depth_texture(self.game.resolution_combat_particles)
        # Create a framebuffer we can render to
        self.alpha_offscreen = self.ctx.framebuffer(
            color_attachments=[self.alpha_diffuse,], depth_attachment=self.alpha_depth,
        )
        # Create a framebuffer we can render to
        self.solid_offscreen = self.ctx.framebuffer(
            color_attachments=[self.solid_diffuse,], depth_attachment=self.alpha_depth,
        )

    def get_loc_fighter(self, team, base):
        if team == 1:
            l = self.location_team1
        else:
            l = self.location_team0

        return (l[0] * base[0], l[1] * base[1], l[2] * base[2])

    @property
    def location_team0(self):
        return self.bmove.t0

    @property
    def location_team1(self):
        return self.bmove.t1

    def set_pokemon(self, spriteset, team):
        if team == 0:
            self.poke1_set = spriteset
            # self.poke1_set = self.game.m_res.prepare_battle_animset(
            #     f"{str(id).zfill(3)}"
            # )
        else:
            self.poke2_set = spriteset
            # self.poke2_set = self.game.m_res.prepare_battle_animset(
            #     f"{str(id).zfill(3)}"
            # )

    def set_dark(self, dark, speed, recover):
        self.dark_recover = recover
        if speed is not None:
            self.dark_to = dark
            self.dark_speed = speed
            if self.dark_to > self.dark:
                self.dark_direction = 1
            else:
                self.dark_direction = -1
        else:
            self.dark_to = None
            self.dark_speed = None
            self.dark = dark

    def set_movement(self, team, position, speed, recover):
        self.bmove.set_movement(team, position, speed, recover)

    def do_particle(self, name, user, target, miss=False):
        if name:
            name = name.replace(" ", "-")
            if miss:
                # TODO Particles miss to left/right
                pass
            self.game.m_par.spawn_system(self, name, target, miss)  # name)
        else:
            print("Empty particle!")

    def render(self, time: float, frame_time: float):
        self.bmove.render(time, frame_time)
        if self.dark_to is not None:
            self.dark = max(
                self.dark + frame_time / 2 * self.dark_speed * self.dark_direction, 0
            )

            if (self.dark - self.dark_to) * self.dark_direction > 0.01:
                self.dark = self.dark_to
                self.dark_to = None

        elif self.dark_recover:
            self.dark = min(self.dark + frame_time / 2.5, 1)

        self.battle_shake = min(self.battle_shake + frame_time / 2, 1)
        self.prog_bg["Brightness"] = self.dark
        self.render_prog["Contrast"] = 3.0 - 2 * self.dark
        self.camera.shake_value = ((1.0 - self.battle_shake) / 2) ** 3.0
        self.prog_bg["Shake"] = self.camera.shake
        self.render_prog["Shake"] = self.camera.shake
        self.prog["Shake"] = self.camera.shake * 6  # TODO: this is a temporary fix

        # TODO
        """redo:
        1. draw background and char on screen
        2. draw trans char on offscreen
        3. draw solids on offscreen
        4. draw offscreen (solids) on screen
        5. lock depth
        6. reset offscreen (not resetting depth)
        7. draw alphas on offscreen
        8. draw offscreen (alphas) on screen
        """
        self.game.m_par.battle = self  # TODO: this is stupid

        # Init perspective
        self.camera.render(time, frame_time)

        # Clear
        self.ctx.clear()
        self.alpha_offscreen.clear(0.0, 0.0, 0.0, 0.0)
        self.solid_offscreen.clear(0.0, 0.0, 0.0, 0.0)

        # Render main screen base
        self.render_background()
        self.ctx.depth_func = "1"
        self.render_pokemon(time, frame_time, cutout=False, shadow=True)
        self.render_pokemon(time, frame_time, cutout=False)
        self.ctx.depth_func = "<="

        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.ctx.blend_equation = moderngl.FUNC_ADD

        # Render black cutout
        # self.solid_offscreen.use()
        # self.render_pokemon(cutout=True)
        self.alpha_offscreen.use()
        self.render_pokemon(time, frame_time, cutout=True)

        # Render
        locking = self.game.m_par.on_tick(time, frame_time, self.alpha_offscreen)

        # ### Aggregate picture
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.ctx.blend_equation = moderngl.FUNC_ADD
        self.game.offscreen.use()

        # Solid
        self.ctx.disable(moderngl.BLEND)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.solid_diffuse.use(location=0)
        self.quad_fs.render(self.render_prog)

        # Alpha
        self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE
        self.alpha_diffuse.use(location=0)
        self.quad_fs.render(self.render_prog)

        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.ctx.blend_equation = moderngl.FUNC_ADD
        return locking

    def render_background(self):
        self.ctx.enable(moderngl.BLEND)

        for tex in self.environment:
            self.prog_bg["Texture"] = 0
            tex.use(0)
            speed = tex.size[0] / tex.size[1] / 16 * 9
            self.prog_bg["Speed"] = speed
            self.prog_bg["Offset"].value = self.camera.parallax_rotation * speed
            self.quad_fs.render(self.prog_bg)

    def render_pokemon(self, time, frame_time, cutout=False, shadow=False):
        if not cutout:
            for i in range(len(self.brightness)):
                self.brightness[i] += 10 * frame_time * (1.0 - self.brightness[i])

        self.prog["CameraPosition"] = self.game.m_cam.pos
        self.prog["Cutout"] = cutout
        self.prog["IsShadow"] = shadow
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)

        self.prog["BillboardFace"].write((self.camera.bill_rot).astype("f4").tobytes())

        self.prog["Mvp"].write((self.camera.mvp).astype("f4").tobytes())

        enemy_first = not (int((self.camera.rotation_value + 2) % 4) % 3)
        if self.poke2_set and enemy_first:
            # TODO: support >2 chars
            self.prog["Brightness"] = ((1.5 - self.brightness[1]) * 2) ** 1.2
            self.vbo_pkm.write(
                np.asarray(
                    [
                        self.camera.pos[0]
                        + self.location_team1[0] * self.character_offset,
                        self.camera.pos[1]
                        + self.location_team1[1] * self.character_offset,
                        self.camera.pos[2]
                        + self.location_team1[2] * self.character_offset,
                    ],
                    dtype="f4",
                ),
                offset=0,
            )
            self.prog["Texture"] = 0
            face = int((self.camera.rotation_value + 2) % 4)
            l = (
                self.poke2_set[0 if face % 3 else 1][0].size[0]
                // self.poke2_set[0 if face % 3 else 1][0].size[1]
            )
            self.prog["Size"] = (
                self.poke2_set[0 if face % 3 else 1][0].size[1] / 4
            ) ** 0.5
            self.prog["AnimationFrame"] = int(time * 8) % l
            self.prog["AnimationLength"] = l
            self.prog["HeightShare"] = self.poke2_set[0 if face % 3 else 1][1]
            self.prog["Mirror"] = -1 if face % 2 else 1

            self.poke2_set[0 if face % 3 else 1][0].use(location=0)
            self.vao_pkm.render(moderngl.POINTS, vertices=1)

        if self.poke1_set:
            self.prog["Brightness"] = self.brightness[0]
            self.vbo_pkm.write(
                np.asarray(
                    [
                        self.camera.pos[0]
                        + self.location_team0[0] * self.character_offset,
                        self.camera.pos[1]
                        + self.location_team0[1] * self.character_offset,
                        self.camera.pos[2]
                        + self.location_team0[2] * self.character_offset,
                    ],
                    dtype="f4",
                ),
                offset=0,
            )
            face = int((self.camera.rotation_value) % 4)
            l = (
                self.poke1_set[0 if face % 3 else 1][0].size[0]
                // self.poke1_set[0 if face % 3 else 1][0].size[1]
            )
            self.prog["Size"] = (
                self.poke1_set[0 if face % 3 else 1][0].size[1] / 4
            ) ** 0.5
            self.prog["AnimationFrame"] = int(time * 8) % l
            self.prog["AnimationLength"] = l
            self.prog["HeightShare"] = self.poke1_set[0 if face % 3 else 1][1]
            self.prog["Mirror"] = -1 if face % 2 else 1

            self.poke1_set[0 if face % 3 else 1][0].use(location=0)
            self.vao_pkm.render(moderngl.POINTS, vertices=1)

        # TODO: remove duplicate
        if self.poke2_set and not enemy_first:
            # TODO: support >2 chars
            self.prog["Brightness"] = ((1.5 - self.brightness[1]) * 2) ** 1.2
            self.vbo_pkm.write(
                np.asarray(
                    [
                        self.camera.pos[0]
                        + self.location_team1[0] * self.character_offset,
                        self.camera.pos[1]
                        + self.location_team1[1] * self.character_offset,
                        self.camera.pos[2]
                        + self.location_team1[2] * self.character_offset,
                    ],
                    dtype="f4",
                ),
                offset=0,
            )
            self.prog["Texture"] = 0
            face = int((self.camera.rotation_value + 2) % 4)
            l = (
                self.poke2_set[0 if face % 3 else 1][0].size[0]
                // self.poke2_set[0 if face % 3 else 1][0].size[1]
            )
            self.prog["Size"] = (
                self.poke2_set[0 if face % 3 else 1][0].size[1] / 4
            ) ** 0.5
            self.prog["AnimationFrame"] = int(time * 8) % l
            self.prog["AnimationLength"] = l
            self.prog["HeightShare"] = self.poke2_set[0 if face % 3 else 1][1]
            self.prog["Mirror"] = -1 if face % 2 else 1

            self.poke2_set[0 if face % 3 else 1][0].use(location=0)
            self.vao_pkm.render(moderngl.POINTS, vertices=1)

        self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
