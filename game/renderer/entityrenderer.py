import moderngl
from PIL import Image
from array import array
import numpy as np

# Max amount of entities!
ENTITYCOUNT = 1024


class EntityRenderer:
    def __init__(self, game, ctx):
        self.game = game
        self.ctx = ctx

        self.amount_of_entities = 0
        self.prog_entities = self.game.m_res.get_program("map_entity")

        self.prog_entities["WindowSize"] = self.game.size

        self.vbo_entities = self.ctx.buffer(
            b"".join(
                np.array([0, 0, 0, 0, 0, 0, 0]).astype("f4").tobytes()
                for i in range(ENTITYCOUNT)
            )
        )

        self.vao_entities = self.ctx.vertex_array(
            self.prog_entities, [(self.vbo_entities, "3f 4f", "in_vert", "in_anim"),]
        )
        self.idx = 0
        self.texture_size_map = []

    def render(self, height):
        # self.text_texture.use()
        self.prog_entities["LayerHeight"] = height
        self.tarray_entities.use()
        self.vao_entities.render(moderngl.POINTS, self.amount_of_entities)

    def pan(self, pos, zoom):
        self.prog_entities["WindowPosition"] = (pos[0], pos[1])
        self.prog_entities["Zoom"] = zoom[0] * 20  # (1 / zoom[0]) / 20

    def set_texture_map(self, l):
        array_list = []
        max_x = 0
        max_y = 0
        self.texture_size_map = []

        for x in l:
            # TODO move to resource manager ipv just reference
            # print("SET TEXTURE MAP")
            # print(x)
            arr = np.array(Image.open(x))
            array_list.append(arr)

            # print(arr.shape)
            max_x = max(max_x, arr.shape[0])
            max_y = max(max_y, arr.shape[1])
            self.texture_size_map.append(arr.shape[:2])

        output_list = []
        for img in array_list:
            arr = np.zeros((max_x, max_y, 4))
            x, y, _ = img.shape
            arr[:x, :y] = img
            output_list.append(arr)

        matrix = np.stack(output_list).astype("uint8")
        mbytes = matrix.tobytes()

        # print("ENTITY SHAPE", matrix.shape)
        # print("ENTITY SPRITES:", (matrix.shape[2], matrix.shape[1], matrix.shape[0]))
        self.tarray_entities = self.ctx.texture_array(
            (matrix.shape[2], matrix.shape[1], matrix.shape[0]), 4, mbytes,
        )
        self.tarray_entities.filter = moderngl.NEAREST, moderngl.NEAREST
        self.tarray_entities.write(mbytes)
        self.tarray_entities.use()
        self.prog_entities["TextureSize"] = (max_x, max_y)

    def set_entity_info(self, l):
        e_l = []
        for pair in l:
            sizemap = self.texture_size_map[pair[3]]
            # print(sizemap[0] // 8, sizemap[0] // 6)
            # TODO: make exact
            pair[1] = pair[1] - sizemap[0] // 10 + 10  # 32 - 1
            e_l.extend(pair)
            e_l.extend(sizemap)

        self.vbo_entities.write(np.array(e_l).astype("f4").tobytes())
        self.amount_of_entities = len(e_l) // 7
