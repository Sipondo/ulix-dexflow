import json

import numpy as np

from io import BytesIO
from pathlib import Path

from kivy.resources import resource_find, resource_add_path, resource_remove_path
from kivy.core.image import Image

# from PIL import Image, ImageFont


TYPES = [
    "NORMAL",
    "FIGHTING",
    "FLYING",
    "POISON",
    "GROUND",
    "ROCK",
    "BUG",
    "GHOST",
    "STEEL",
    "UNKNOWN",
    "FIRE",
    "WATER",
    "GRASS",
    "ELECTRIC",
    "PSYCHIC",
    "ICE",
    "DRAGON",
    "DARK",
    "FAIRY",
]


class ResourceManager:
    def __init__(self, game):
        self.game = game
        self.resource_dirs = list(Path("").glob("resources/*/"))

        # for dir in self.resource_dirs:
        #     if dir.is_dir():
        #         resources.register_dir(dir.resolve())

        self.p_shaders = Path("shader")
        self.p_graphics = Path("graphics")
        self.p_icons = self.p_graphics / "icon"
        self.p_items = self.p_graphics / "items"
        self.p_interface = self.p_graphics / "interface"
        self.p_picture = self.p_graphics / "pictures"
        self.p_trainers = self.p_graphics / "trainers"
        self.p_fonts = Path("font")
        self.p_sprites = self.p_graphics / "characters"
        self.p_audio = Path("audio")
        self.p_particle = Path("particle")

        self.p_pbs = Path("pbs")
        self.p_pbs_c = self.p_pbs / "compressed"

        self.tilesets = {}
        self.programs = {}

        self.fighter_splashes = {}
        self.fighter_icons = {}

        self.noise = None

        self.audiocache = {}

        self.raw_types = TYPES

    def get_pbs_loc(self, name, compressed=False):
        if compressed:
            pth = self.p_pbs_c / name
        else:
            pth = self.p_pbs / name
        return self.resolve_resource_path(pth)

    def resolve_resource_path(self, pth):
        for dir in self.resource_dirs:
            # if (dir / pth).is_file():
            #     return dir / pth
            if d := resource_find(str(dir / pth)):
                return d
        return None

    def get_shader(self, program_name):
        with open(resource_find(f"resources/base/shader/{program_name}.glsl")) as file:
            return file.read()

    def get_shader_geoblocks(self, vertex_name, geo_name, geoblocks, uniforms):
        # print(vertex_name, geoblocks)
        vs = self.get_shader(vertex_name)
        gs = (
            self.get_shader(geo_name)
            .replace(r"%GEOBLOCKS%", geoblocks)
            .replace(r"%UNIFORMS%", uniforms)
        )

        return vs, gs

    def get_particle(self, pth, move_data=None):
        try:
            pth = self.resolve_resource_path(self.p_particle / (pth + ".json"))
            if pth:
                with open(pth) as f:
                    return json.load(f)
        except Exception as e:
            pass
            # traceback.print_exc()

        try:
            if move_data is not None:
                if int(move_data.power) < 5:
                    pth = self.resolve_resource_path(
                        self.p_particle / ("generic-powerless.json")
                    )
                else:
                    print("Search path")
                    pth = self.resolve_resource_path(
                        self.p_particle
                        / (
                            f"{self.game.m_pbs.get_related_anim(move_data.type, move_data.power)}.json"
                        )
                    )
                    print(pth)
                if pth:
                    with open(pth) as f:
                        return json.load(f)
        except Exception as e:
            raise e
            pass
            # traceback.print_exc()

        pth = self.resolve_resource_path(self.p_particle / ("generic-powerless.json"))
        with open(pth) as f:
            return json.load(f)

    def get_geoblock(self, geoblock_name):
        with open(
            resource_find(f"resources/base/shader/p5geoblocks/{geoblock_name}.glsl")
        ) as geoblock:
            return geoblock.read()

    def get_texture(self, category, name):
        pth = self.p_graphics / category / (Path(name).stem + ".png")
        pth = self.resolve_resource_path(pth)
        return Image.load(pth).texture

    #############################
    #############################
    #############################
    #############################
    #############################
    #############################
    ############################# LINE OF DEPRECATION
    #############################
    #############################
    #############################
    #############################
    #############################
    #############################

    def init_types(self):
        types = self.open_image_interface(
            self.p_graphics / "pictures" / "types.png", size=0.5
        )
        w, h = types.size
        icon_height = h // len(TYPES)
        self.types = {
            k: v
            for k, v in zip(
                TYPES,
                [
                    types.crop((0, i * icon_height, w, (i + 1) * icon_height))
                    for i in range(len(TYPES))
                ],
            )
        }

        # self.attack_types = {
        #     x: self.get_interface(f"attack_types/attack_{x.lower()}") for x in TYPES
        # }
        self.attack_types = {
            x.lower(): f"attack_types/attack_{x.lower()}" for x in TYPES
        }

    def get_font(self, name, scale):
        pth = (self.p_fonts / Path(name).stem).with_suffix(".ttf")
        pth = self.resolve_resource_path(pth)
        return str(pth)
        return freetype.Face(str(pth))
        return {
            x: ImageFont.truetype(str(pth.resolve()), x * scale)
            for x in range(6, 20, 2)
        }

    def get_entity_textures(self):
        paths = []
        names = []
        for dir in self.resource_dirs:
            for file in (dir / self.p_sprites).glob("*.png"):
                if file.stem not in names:
                    paths.append(file)
                    names.append(file.stem)
        return (paths, names)

    # def get_splash(self, resource_name):
    #     return self.open_image(self.p_graphics / "splash" / f"{resource_name}.png")

    def get_sprite(self, resource_name, sub="", size=1):
        return self.open_image_interface(
            self.p_graphics / "sprite" / sub / f"{str(resource_name).zfill(3)}.png",
            size,
        )

    def get_sprite_from_anim(self, resource_name, size=1):
        if f"{resource_name}___{size}" not in self.fighter_splashes:
            pth = (
                self.p_graphics
                / "pokemon_anim"
                / "front"
                / f"{str(resource_name).zfill(3)}.png"
            )
            img = self.open_image_interface(pth, size,)
            w, h = img.size
            self.fighter_splashes[f"{resource_name}___{size}"] = img.crop((0, 0, h, h))
        return self.fighter_splashes[f"{resource_name}___{size}"]

    def get_party_icon(self, resource_name, size=1.0):
        if f"{resource_name}___{size}" not in self.fighter_icons:
            img = self.open_image_interface(
                self.p_graphics / "pokemon_icons" / f"{resource_name}.png", size,
            )
            w, h = img.size
            self.fighter_icons[f"{resource_name}___{size}"] = (
                img.crop((0, 0, w // 2, h)),
                img.crop((w // 2, 0, w, h)),
            )
        return self.fighter_icons[f"{resource_name}___{size}"]

    def get_item_icon(self, resource_name, size=1):
        pth = self.p_items / f"{str(resource_name)}.png"
        if self.resolve_resource_path(pth):
            return self.open_image_interface(pth, size,).convert("RGBA")
        return self.open_image_interface(self.p_items / "000.png", size,).convert(
            "RGBA"
        )

    def get_interface(self, resource_name, size=0.5):
        resource_name = resource_name.lower()
        if "trainers/" in resource_name:
            pth = self.p_trainers / f"{str(Path(resource_name).stem)}.png"
        elif "icon/" in resource_name:
            return self.get_party_icon(Path(resource_name).stem, size)
        elif "sprite/" in resource_name:
            return self.get_sprite_from_anim(Path(resource_name).stem, size)
        elif "item/" in resource_name:
            return self.get_item_icon(Path(resource_name).stem, size)
        else:
            pth = self.p_interface / f"{str(resource_name)}.png"

        if self.resolve_resource_path(pth):
            return self.open_image_interface(pth, size,).convert("RGBA")
        return self.open_image_interface(self.p_items / "000.png", size,).convert(
            "RGBA"
        )

    def get_picture(self, resource_name, size=0.5):
        pth = self.p_picture / f"{str(resource_name)}.png"
        if self.resolve_resource_path(pth):
            return self.open_image_interface(pth, size,).convert("RGBA")
        return self.open_image_interface(self.p_items / "000.png", size,).convert(
            "RGBA"
        )

    def get_trainer_splash(self, resource_name, size=0.5):
        pth = self.p_trainers / f"{str(resource_name)}.png"
        if self.resolve_resource_path(pth):
            return self.open_image_interface(pth, size,).convert("RGBA")
        return None

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

    def get_tileset(self, name: str):
        if name not in self.tilesets:
            pth = self.p_graphics / Path(name).with_suffix(".png")
            pth = self.resolve_resource_path(pth)
            sprite = Image.open(pth).convert("RGBA")
            spritemap = sprite.tobytes()
            texture_spritemap = self.ctx.texture(sprite.size, 4, spritemap)
            texture_spritemap.repeat_x = True
            texture_spritemap.repeat_y = True
            texture_spritemap.filter = moderngl.NEAREST, moderngl.NEAREST
            texture_spritemap.write(spritemap)
            self.tilesets[name] = texture_spritemap
        return self.tilesets[name]

    def get_slide_tileset(self, name: str):
        if name not in self.tilesets:
            pth = self.p_graphics / Path(name).with_suffix(".png")
            pth = self.resolve_resource_path(pth)
            pth_list = list(
                pth.parent.glob("_".join(pth.stem.split("_")[:-2] + ["*.png"]))
            )

            sprite_list = []
            for image_pth in pth_list:
                sprite_list.append(np.array(Image.open(image_pth).convert("RGBA")))

            sprite = np.stack(sprite_list).astype("uint8")

            spritemap = sprite.tobytes()
            texture_spritemap = self.ctx.texture_array(
                (sprite.shape[2], sprite.shape[1], sprite.shape[0]), 4, spritemap
            )
            texture_spritemap.repeat_x = True
            texture_spritemap.repeat_y = True
            texture_spritemap.filter = moderngl.NEAREST, moderngl.NEAREST
            texture_spritemap.write(spritemap)
            self.tilesets[name] = texture_spritemap
        return self.tilesets[name]

    def get_program_varyings(
        self, vertex_name, geo_name=None, geoblocks=None, uniforms=None, varyings=[]
    ):
        # print(vertex_name, geoblocks)
        with open(
            self.resolve_resource_path(self.p_shaders / f"{vertex_name}.glsl")
        ) as file_ver:
            if not geo_name:
                # print(f"LOADING SHADER VARYINGS: {vertex_name}.glsl\n\n")
                return self.ctx.program(
                    vertex_shader=file_ver.read(), varyings=varyings,
                )
            if geoblocks is None:
                with open(
                    self.resolve_resource_path(self.p_shaders / f"{geo_name}.glsl")
                ) as file_geo:
                    # print(f"LOADING SHADER VARYINGS: {geo_name}.glsl\n\n")
                    return self.ctx.program(
                        vertex_shader=file_ver.read(),
                        geometry_shader=file_geo.read(),
                        varyings=varyings,
                    )
            with open(
                self.resolve_resource_path(self.p_shaders / f"{geo_name}.glsl")
            ) as file_geo:
                # print(f"LOADING SHADER VARYINGS: {geo_name}.glsl\n\n")
                geo = (
                    file_geo.read()
                    .replace(r"%GEOBLOCKS%", geoblocks)
                    .replace(r"%UNIFORMS%", uniforms)
                )
                return self.ctx.program(
                    vertex_shader=file_ver.read(),
                    geometry_shader=geo,
                    varyings=varyings,
                )

    def get_environment(self, name):
        pth = self.p_graphics / "environments"
        environment = []
        for dir in self.resource_dirs:
            environment.extend(
                [
                    self.game.load_texture_2d(x)
                    for x in (dir / pth).glob(f"{name}_*.png")
                ]
            )
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
        print("SPRITE:", pth)
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
        root = self.p_graphics / "pokemon_anim"
        spriteset = []
        spriteset.append(self.prepare_battle_sprite(root / f"back/{id}.png"))
        spriteset.append(self.prepare_battle_sprite(root / f"front/{id}.png"))
        return spriteset

    def open_image(self, pth, size=1):
        pth = self.resolve_resource_path(pth)
        img = Image.open(pth).convert("RGBA")
        img = img.resize(
            (int(img.size[0] * size), int(img.size[1] * size)), resample=Image.NEAREST
        )
        return img

    def open_image_interface(self, pth, size=1):
        return self.open_image(pth, size * self.game.r_int.scale)

    def prep_image(self, img):
        return img.reshape(((4, img.shape[1], img.shape[0])))

    def get_sound(self, pth):
        pth = self.p_audio / pth
        pth = self.resolve_resource_path(pth)
        if pth is None:
            return pth
        if pth.stem not in self.audiocache:
            self.audiocache[pth.stem] = pyglet.media.load(str(pth), streaming=False)
        return self.audiocache[pth.stem]

    def get_world_data(self):
        pth = Path("world.ldtkc")
        with open(pth, "rb") as file:
            return np.load(BytesIO(file.read()), allow_pickle=True)
