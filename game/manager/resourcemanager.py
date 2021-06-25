import moderngl
import pyglet

import numpy as np

from io import BytesIO
from moderngl import Texture
from moderngl_window import resources
from pathlib import Path
from PIL import Image, ImageFont

pyglet.options["audio"] = ("openal", "pulse", "directsound", "silent")


class ResourceManager:
    def __init__(self, game, ctx):
        self.game = game
        self.ctx = ctx
        self.resource_dirs = list(Path("").glob("resources/*/"))

        for dir in self.resource_dirs:
            if dir.is_dir():
                resources.register_dir(dir.resolve())

        self.p_shaders = Path("shader")
        self.p_graphics = Path("graphics")
        self.p_icons = self.p_graphics / "icon"
        self.p_items = self.p_graphics / "Items"
        self.p_fonts = Path("font")
        self.p_sprites = self.p_graphics / "characters_temp"
        self.p_audio = Path("audio")

        self.p_pbs = Path("pbs")
        self.p_pbs_c = self.p_pbs / "compressed"

        self.tilesets = {}
        self.programs = {}

        self.noise = None

        self.audiocache = {}

    def init_types(self):
        types = self.open_image_interface(
            self.p_graphics / "Pictures" / "Pokedex" / f"icon_types.png"
        )
        w, h = types.size
        self.types = [types.crop((0, 0, w, i * 14)) for i in range(h // 14)]

    def get_font(self, name, scale):
        pth = (self.p_fonts / Path(name).stem).with_suffix(".ttf")
        pth = self.resolve_resource_path(pth)
        return {
            x: ImageFont.truetype(str(pth.resolve()), x * scale)
            for x in range(8, 20, 2)
        }

    def get_entity_textures(self):
        paths = []
        names = []
        for dir in self.resource_dirs:
            for file in (dir / self.p_sprites).glob("*.png"):
                if file.stem not in names:
                    paths.append(file)
                    names.append(file.stem)
        print(names)
        return (paths, names)

    # def get_splash(self, resource_name):
    #     return self.open_image(self.p_graphics / "splash" / f"{resource_name}.png")

    def get_sprite(self, resource_name, sub="", size=1):
        return self.open_image_interface(
            self.p_graphics / "sprite" / sub / f"{str(resource_name).zfill(3)}.png",
            size,
        )

    def get_sprite_from_anim(self, resource_name, size=1):
        pth = (
            self.p_graphics
            / "Pokemon_anim"
            / "Front"
            / f"{str(resource_name).zfill(3)}.png"
        )
        img = self.open_image_interface(pth, size,)
        w, h = img.size
        return img.crop((0, 0, h, h))

    def get_party_icon(self, resource_name, size=1):
        img = self.open_image_interface(
            self.p_graphics
            / "Pokemon"
            / "Icons"
            / f"{str(resource_name).zfill(3)}.png",
            size,
        )
        w, h = img.size
        return img.crop((0, 0, w // 2, h)), img.crop((w // 2, 0, w, h))

    def get_item_icon(self, resource_name, size=1):
        pth = self.p_items / f"{str(resource_name)}.png"
        if pth.is_file():
            return self.open_image_interface(pth, size,).convert("RGBA")
        return self.open_image_interface(self.p_items / "000.png", size,).convert(
            "RGBA"
        )

    def get_splash(self, resource_name, size=1):
        pth = self.p_graphics / "splash" / f"{str(resource_name)}.png"
        return self.open_image_interface(pth, size,).convert("RGBA")

    def get_sprite_tiled(self, ts, resource_name, sub="", size=1):
        # TODO: dit is retarded
        sheet = self.get_sprite(resource_name, sub, size)
        sprite_list = []

        for j in range(int(sheet.shape[1]) // ts[0]):
            for i in range(int(sheet.shape[0]) // ts[1]):
                sprite_list.append(
                    sheet[j * ts[1] : (j + 1) * ts[1], i * ts[0] : (i + 1) * ts[0]]
                )
        return np.array(sprite_list)

    def get_tileset(self, name: str) -> Texture:
        if name not in self.tilesets:
            pth = self.p_graphics / Path(name).with_suffix(".png")
            pth = self.resolve_resource_path(pth)
            sprite = Image.open(pth)
            spritemap = sprite.tobytes()
            texture_spritemap = self.ctx.texture(sprite.size, 4, spritemap)
            texture_spritemap.repeat_x = True
            texture_spritemap.repeat_y = True
            texture_spritemap.filter = moderngl.NEAREST, moderngl.NEAREST
            texture_spritemap.write(spritemap)
            self.tilesets[name] = texture_spritemap
        return self.tilesets[name]

    def get_program(self, program_name):
        return self.game.load_program(self.p_shaders / f"{program_name}.glsl")

    def get_program_varyings(
        self, vertex_name, geo_name=None, geoblocks=None, uniforms=None, varyings=[]
    ):
        # print(vertex_name, geoblocks)
        with open(self.p_shaders / f"{vertex_name}.glsl") as file_ver:
            if not geo_name:
                # print(f"LOADING SHADER VARYINGS: {vertex_name}.glsl\n\n")
                return self.ctx.program(
                    vertex_shader=file_ver.read(), varyings=varyings,
                )
            if geoblocks is None:
                with open(self.p_shaders / f"{geo_name}.glsl") as file_geo:
                    # print(f"LOADING SHADER VARYINGS: {geo_name}.glsl\n\n")
                    return self.ctx.program(
                        vertex_shader=file_ver.read(),
                        geometry_shader=file_geo.read(),
                        varyings=varyings,
                    )
            with open(self.p_shaders / f"{geo_name}.glsl") as file_geo:
                # print(f"LOADING SHADER VARYINGS: {geo_name}.glsl\n\n")
                geo = (
                    file_geo.read()
                    .replace(r"%GEOBLOCKS%", geoblocks)
                    .replace(r"%UNIFORMS%", uniforms)
                )
                print(geo)
                return self.ctx.program(
                    vertex_shader=file_ver.read(),
                    geometry_shader=geo,
                    varyings=varyings,
                )

    def get_geoblock(self, geoblock_name):
        with open(self.p_shaders / "p4geoblocks" / f"{geoblock_name}.glsl") as geoblock:
            return geoblock.read()

    def get_texture(self, category, name):
        pth = self.p_graphics / category / Path(name).stem.with_suffix(".png")
        pth = self.resolve_resource_path(pth)
        return self.game.load_texture_2d(pth)

    def get_environment(self, name):
        pth = self.p_graphics / "environments"
        pth = self.resolve_resource_path(pth)
        environment = [self.game.load_texture_2d(x) for x in pth.glob(f"{name}_*.png")]
        for env in environment:
            env.filter = (moderngl.NEAREST, moderngl.NEAREST)
        environment.reverse()
        return environment

    def get_noise(self):
        return self.noise

    def init_noise(self):
        self.noise = self.game.load_texture_array(
            self.p_graphics / "particle_mask" / "noise.png", layers=755
        )

    def prepare_battle_sprite(self, pth, mirror=False):
        a = self.open_image(pth)
        a = np.flip(a, axis=0)

        b = a[:, : a.shape[0], 3]
        s = np.amax((b > 250), axis=0)
        height = np.amin((b[:, s] > 250).argmax(axis=0))
        height_share = (a.shape[0] - height) / a.shape[0]

        a = self.prep_image(a)

        texture = self.ctx.texture(a.shape[1:], 4, a.tobytes())
        texture.filter = (moderngl.LINEAR, moderngl.NEAREST)
        texture.write(a.tobytes())
        return texture, height_share

    def prepare_battle_animset(self, id):
        root = "resources/graphics/Pokemon_anim/"
        spriteset = []
        spriteset.append(self.prepare_battle_sprite(f"{root}Back/{id}.png"))
        spriteset.append(self.prepare_battle_sprite(f"{root}Front/{id}.png"))
        return spriteset

    def open_image(self, pth, size=1):
        pth = self.resolve_resource_path(pth)
        img = Image.open(pth)
        img = img.resize(
            (int(img.size[0] * size), int(img.size[1] * size)), resample=Image.NEAREST
        )
        return img

    def open_image_interface(self, pth, size=1):
        return self.open_image(pth, size * self.game.r_int.scale)

    def prep_image(self, img):
        return img.reshape(((4, img.shape[1], img.shape[0])))

    def get_sound(self, pth):
        pth = self.resolve_resource_path(pth)
        if pth.stem not in self.audiocache:
            self.audiocache[pth.stem] = pyglet.media.load(
                str(self.p_audio / pth), streaming=False
            )
        return self.audiocache[pth.stem]

    def get_world_data(self):
        pth = Path("world/world.ldtkc")
        with open(pth, "rb") as file:
            return np.load(BytesIO(file.read()), allow_pickle=True)

    def resolve_resource_path(self, pth):
        for dir in self.resource_dirs:
            if (dir / pth).is_file():
                return dir / pth
        return None

    def get_pbs_loc(self, name, compressed=False):
        if compressed:
            pth = self.p_pbs_c / name
        else:
            pth = self.p_pbs / name
        return self.resolve_resource_path(pth)
