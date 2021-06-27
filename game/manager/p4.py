from game.particle.p4system import ParticleSystem
import moderngl


class ParticleManager:
    def __init__(self, game):
        self.battle = None
        self.game = game
        self.ctx = self.game.ctx
        self.systems = []
        self.step_quantity = 240
        self.step_size = 1 / self.step_quantity

        self.floats = 16
        self.stride = self.floats * 4

        self.fast_forward = False

    def on_tick(self, time, frame_time, alpha_target, anti_target):
        frame_time = min(2, max(0.0001, frame_time))
        self.alpha_target = alpha_target
        self.anti_target = anti_target
        busy = False

        marked = []
        for system in self.systems:
            succes = system.on_tick(time, frame_time)
            busy = busy or succes
            if not succes:
                marked.append(system)

        for system in marked:
            self.systems.remove(system)
            del system
        return busy

    def set_render(self, t):
        if t == 1:
            self.battle.solid_offscreen.use()
            self.battle.solid_offscreen.depth_mask = True
            self.ctx.disable(moderngl.BLEND)
            self.ctx.enable(moderngl.CULL_FACE | moderngl.DEPTH_TEST | moderngl.BLEND)
            return
        if t == 2:
            self.battle.alpha_offscreen.use()
            self.ctx.enable(moderngl.BLEND | moderngl.DEPTH_TEST | moderngl.CULL_FACE)
            self.ctx.blend_func = moderngl.ADDITIVE_BLENDING
            self.ctx.blend_equation = moderngl.FUNC_ADD
            self.alpha_target.depth_mask = False
            return
        if t == 3:
            self.game.offscreen.use()
            self.game.offscreen.depth_mask = True
            self.alpha_target.depth_mask = True
            self.anti_target.depth_mask = True
            self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
            self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
            self.ctx.blend_equation = moderngl.FUNC_ADD
            return
        if t == 4:
            self.battle.anti_offscreen.use()
            self.ctx.enable(moderngl.BLEND | moderngl.DEPTH_TEST | moderngl.CULL_FACE)
            self.ctx.blend_func = moderngl.ADDITIVE_BLENDING
            self.ctx.blend_equation = moderngl.FUNC_ADD
            self.anti_target.depth_mask = False
            return

    def spawn_system(self, brender, fname, target, miss):
        if target:
            self.systems.append(ParticleSystem(self.game, brender, fname, target, miss))

    def vao_def(self, buffer, render=False):
        if render:
            return (
                buffer,
                "4f 3x4 1f 3f 1f 1x4 1x4 1f 1x4",
                "in_pos",
                "in_size",
                "in_color",
                "in_rot",
                "in_noise",
            )
        return (
            buffer,
            "4f 3f 1f 3f 1f 1f 1f 1f 1f",
            "in_pos",
            "in_vel",
            "in_size",
            "in_color",
            "in_rot",
            "in_rot_vel",
            "in_lifespan",
            "in_noise",
            "in_key",
        )

    def get_varyings(render=False):
        return [
            "out_pos",
            "out_vel",
            "out_size",
            "out_color",
            "out_rot",
            "out_rot_vel",
            "out_lifespan",
            "out_noise",
            "out_key",
        ]
