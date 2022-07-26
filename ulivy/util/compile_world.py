import json
import logging
import math
import numpy as np

from io import BytesIO
from pathlib import Path

from ulivy.helpers.ldtkjson import ldtk_json_from_dict
from ulivy.upl.uplmanager import UplParser


def compile_world(pth):
    root = Path(pth)

    """
    Compiles world.ldtk into world.ldtkc
    """

    # load editable level file
    with open(root / "world.ldtk", "r", encoding="utf-8") as infile:
        ldtk = json.load(infile)

    # load external levels if present
    if ldtk["externalLevels"]:
        for i, level in enumerate(ldtk["levels"]):
            if level["externalRelPath"]:
                with open(
                    root / level["externalRelPath"], "r", encoding="utf-8"
                ) as infile:
                    ldtk["levels"][i] = json.load(infile)

    # Sets tile enums
    def coldef_to_bool(coldef):
        all = "X" in coldef
        if all:
            return [True, True, True, True] + [x in coldef for x in enumValues]
        return ["E" in coldef, "S" in coldef, "W" in coldef, "N" in coldef,] + [
            x in coldef for x in enumValues
        ]

    a = ldtk_json_from_dict(ldtk)

    defs = a.defs

    ent_field_upl = {
        ent.uid: {
            x.uid: "ruby" in str(x.text_language_mode).lower() for x in ent.field_defs
        }
        for ent in defs.entities
    }
    parser = UplParser()

    all_level_data = {}

    coldefs = {
        t.uid: {
            n: [x.enum_value_id for x in t.enum_tags if n in x.tile_ids]
            for n in range(t.px_hei * t.px_wid // 256)
        }
        for t in a.defs.tilesets
    }

    customData = {t.uid: t.custom_data for t in a.defs.tilesets}

    enumValues = list(
        dict.fromkeys(
            ["E", "S", "W", "N", "X"]
            + [x.enum_value_id for t in a.defs.tilesets for x in t.enum_tags]
        )
    )[5:]

    for enum in [x for x in a.defs.enums if x.identifier in ("Settables")]:
        settables = [x.id.lower() for x in enum.values]

    for enum in [x for x in a.defs.enums if x.identifier in ("Switches")]:
        switches = [x.id.lower() for x in enum.values]

    logging.info("ENUMVALUES:", enumValues)
    logging.info("CUSTOMDATA:", customData)
    logging.info("SETTABLES:", settables)
    logging.info("SWITCHES:", switches)

    for level in a.levels:
        print(level.identifier.lower())
        # if not "l1_happyhouse" in level.identifier.lower():
        #     continue
        logging.info("\n", "-" * 50, f"LEVEL: {level.identifier}", "-" * 50)
        # logging.info({field.identifier: field.value for field in level.field_instances})

        id_e = [int(x[1:]) for x in level.identifier.lower().split("_")[:-1]]
        id = str(id_e[0] * 1000 + (len(id_e) > 1 and id_e[1] or 0))

        last_layer = "init"
        depth = 0
        layer_depths = []
        for layer in level.layer_instances:
            if "Boundaries" in layer.identifier:
                continue
            if last_layer != "init" and last_layer != layer.tileset_rel_path:
                layer_depths.append(depth)
                depth = 0
            depth += 1
            last_layer = layer.tileset_rel_path
        layer_depths.append(depth)
        logging.info(layer_depths)

        # TODO: fix renderer so it doesn't require 16x16 worlds
        orig_width = level.px_wid // 16
        orig_height = level.px_hei // 16
        width = math.ceil(level.px_wid / 256 + 1) * 16
        height = math.ceil(level.px_hei / 256 + 1) * 16

        # TODO: get rid of this hack as well (2^ maps)
        width = 2 ** math.ceil(math.log2(width))
        height = 2 ** math.ceil(math.log2(height))

        reversed_instances = [
            x
            for x in reversed(level.layer_instances)
            if "Boundaries" not in x.identifier
        ]

        current_layer = 0
        entity_height = 0
        output_layers = []

        ################################################################################
        ##################################### TILES ####################################
        ################################################################################

        for index, depth_block in enumerate(reversed(layer_depths)):
            logging.info("Depth Block:", depth_block)
            curinst = reversed_instances[current_layer]

            tileset = curinst.tileset_rel_path and "/".join(
                [
                    x.stem
                    for x in list(Path(curinst.tileset_rel_path).parents)[::-1]
                    if "graphics" in str(x)
                ][1:]
                + [Path(curinst.tileset_rel_path).stem]
            )

            STACK = 10
            if tileset != None:
                tile_array = np.zeros(
                    (depth_block, STACK, height, width, 2), dtype=np.dtype("uint16")
                )
                col_array = np.zeros(
                    (depth_block, STACK, height, width, 9), dtype=np.dtype("bool")
                )
                for current_depth in range(depth_block):
                    layer = reversed_instances[current_layer]
                    logging.info(
                        f"{layer.identifier: <20} - {layer.type: <10} - {layer.tileset_rel_path}"
                    )

                    if layer.type == "Tiles":
                        for tile in layer.grid_tiles:
                            loc = (tile.px[0] // 16, tile.px[1] // 16)

                            stack = 0
                            while (
                                sum(tile_array[current_depth, stack, loc[1], loc[0]])
                                > 0
                            ):
                                stack += 1

                            tile_array[current_depth, stack, loc[1], loc[0]] = (
                                tile.src[0] // 16 + 1,
                                tile.src[1] // 16,
                            )
                            col_array[
                                current_depth, stack, loc[1], loc[0]
                            ] = coldef_to_bool(coldefs[layer.tileset_def_uid][tile.t])
                    if layer.type == "IntGrid":
                        for tile in layer.auto_layer_tiles:
                            loc = (
                                tile.px[0] // 16,
                                tile.px[1] // 16,
                            )

                            stack = 0
                            while (
                                sum(tile_array[current_depth, stack, loc[1], loc[0]])
                                > 0
                            ):
                                stack += 1

                            tile_array[current_depth, stack, loc[1], loc[0]] = (
                                tile.src[0] // 16 + (tile.f % 2) + 1,
                                tile.src[1] // 16 + (tile.f // 2),
                            )
                            col_array[
                                current_depth, stack, loc[1], loc[0]
                            ] = coldef_to_bool(coldefs[layer.tileset_def_uid][tile.t])
                    current_layer += 1
                colmap = col_array[0]
                for individual in col_array[1:]:
                    colmap = colmap | individual

                output_layers.append(["TILES", tileset, tile_array, colmap])
            else:
                logging.info(
                    "IDENTIFIER", reversed_instances[current_layer].identifier.lower()
                )
                if "Regions" in curinst.identifier:
                    output_layers.append(["REGIONS"])
                else:
                    output_layers.append(["ENTITIES", entity_height])
                    entity_height += 1
                current_layer += 1

        atlas_layers = convert_to_atlas_layers(output_layers)

        entities = []
        regions = []

        ################################################################################
        ################################### ENTITIES ###################################
        ################################################################################
        entity_height = 0
        for instance in reversed_instances:
            if instance.type == "Entities":
                if "Regions" in instance.identifier:
                    logging.info(f"Regions: {instance.identifier}")
                    for raw_ent in instance.entity_instances:
                        entity = {}
                        entity["identifier"] = raw_ent.identifier
                        entity["location"] = raw_ent.px
                        for field in raw_ent.field_instances:
                            if ent_field_upl[raw_ent.def_uid][field.def_uid]:
                                entity[f"f_{field.identifier}"] = parser.parse(
                                    field.value
                                )
                                # logging.info(entity[f"f_{field.identifier}"].pretty())
                            else:
                                entity[f"f_{field.identifier}"] = field.value
                        entity["width"] = raw_ent.width
                        entity["height"] = raw_ent.height
                        regions.append(entity)
                else:
                    logging.info(f"Entities: {instance.identifier}")
                    for raw_ent in instance.entity_instances:
                        entity = {}
                        entity["identifier"] = raw_ent.identifier
                        entity["location"] = raw_ent.px
                        for field in raw_ent.field_instances:
                            if isinstance(field.value, str):
                                entity[f"f_{field.identifier}"] = field.value.replace(
                                    "../sprites/characters/", "",
                                ).replace(".png", "")
                                if ent_field_upl[raw_ent.def_uid][field.def_uid]:
                                    entity[f"f_{field.identifier}"] = parser.parse(
                                        entity[f"f_{field.identifier}"]
                                    )
                                    # logging.info(entity[f"f_{field.identifier}"].pretty())
                            else:
                                entity[f"f_{field.identifier}"] = field.value
                        entity["width"] = raw_ent.width
                        entity["height"] = raw_ent.height
                        entity["layer"] = entity_height
                        entities.append(entity)
                    entity_height += 1

        all_level_data[id] = {
            "layers": atlas_layers,
            "p_height": 0,
            "entities": entities,
            "regions": regions,
            "fields": {
                field.identifier: field.value for field in level.field_instances
            },
            "orig_dimensions": (orig_width, orig_height),
        }

        # logging.info("Total tilesets:", [x[0] for x in output_layers])
        # logging.info(
        #     "Total shapes:",
        #     [x[2].shape if x[0] == "TILES" else x for x in output_layers],
        # )
        # logging.info("Player height:", 0)
        # logging.info("Entities", entities)
        # logging.info("Regions:", "\n\n".join([str(x) for x in regions]))
        # logging.info("\n\n\n")

    world_data = {}

    world_data["levels"] = all_level_data
    world_data["world"] = {
        "enumValues": enumValues,
        "settables": settables,
        "switches": switches,
    }

    for i, image in enumerate(atlas_images):
        atlas_image.paste(
            image,
            (
                ((16 * i) // 2048) * 16,
                ((16 * i) % 2048),
                ((16 * i) // 2048) * 16 + 16,
                ((16 * i) % 2048) + 16,
            ),
            image,
        )
    atlas_image.save("data/atlas_tiles.png")

    f = BytesIO()
    np.savez_compressed(f, **world_data)
    f.seek(0)
    out = f.read()

    with open("world.ldtkc", "wb") as file:
        file.write(out)


from PIL import Image

atlas_image = Image.new("RGBA", (2048, 2048))
atlas_stills = []
atlas_images = []
atlas = {}


def convert_to_atlas_layers(layers):
    logging.info("\n" * 5, "-" * 30, "STARTING ATLAS CONVERSION", "-" * 30, "\n" * 3)

    # Identify atlas blocks
    atlas_blocks = []
    atlas_block = []
    for i, layer in enumerate(layers):
        logging.info(layer[0])

        if layer[0] == "TILES":
            atlas_block.append(i)
        if layer[0] == "ENTITIES":
            atlas_blocks.append(atlas_block)
            atlas_block = []
            atlas_blocks.append([i])
    else:
        if atlas_block:
            atlas_blocks.append(atlas_block)
            atlas_block = []

    # Add the empty tile as 0,0
    tile = Image.new("RGBA", (16, 16))
    dat = list(tile.getdata())
    if dat not in atlas_stills:
        atlas_stills.append(dat)
        atlas_images.append(tile)

    n = -1
    tiledict = {
        x: (n := n + 1)
        for x in set([layer[1] for layer in layers if layer[0] == "TILES"])
    }

    tilesets = [0] * len(tiledict)
    for k, v in tiledict.items():
        tilesets[v] = Image.open(resolve_resource_path(f"{k}.png"))

    output = []
    for block in atlas_blocks:
        layer = layers[block[0]]
        if layer[0] == "ENTITIES":
            output.append(layer)
            continue

        tile_array = layer[2]
        y_range = tile_array.shape[2]
        x_range = tile_array.shape[3]

        output_tile_array = np.zeros((1, y_range, x_range, 2), dtype=np.dtype("uint16"))

        for y in range(y_range):
            for x in range(x_range):
                tile_indices = []
                for layer_i in block:
                    layer_2 = layers[layer_i]
                    tileset_index = tiledict[layer_2[1]]
                    # tileset = tilesets[tileset_index]

                    tile_array = layer_2[2]
                    for depth in range(tile_array.shape[0]):
                        for stack in range(tile_array.shape[1]):
                            tile_index = tile_array[depth, stack, y, x]
                            if tile_index[0] == 0 and tile_index[1] == 0:
                                continue
                            tile_indices.append(
                                (tile_index[0], tile_index[1], tileset_index)
                            )

                    if not tile_indices:
                        continue

                origin = "".join([str(tile_index) for tile_index in tile_indices])

                if origin not in atlas.keys():
                    tile = Image.new("RGBA", (16, 16))

                    for tile_index in tile_indices:
                        tile_index = (tile_index[0] - 1, tile_index[1], tile_index[2])
                        overlay = tilesets[tile_index[2]].crop(
                            (
                                tile_index[0] * 16,
                                tile_index[1] * 16,
                                (tile_index[0] + 1) * 16,
                                (tile_index[1] + 1) * 16,
                            )
                        )
                        tile.paste(overlay, (0, 0), overlay)
                        # tile.save(f"data/tile{tile_index[0]}-{tile_index[1]}.png")

                    dat = list(tile.getdata())
                    # for example in atlas_stills:
                    #     if dat == example:
                    #         break
                    if dat not in atlas_stills:
                        atlas_stills.append(dat)
                        atlas_images.append(tile)
                        # tile.save(f"data/{origin}.png")

                    atlas[origin] = atlas_stills.index(dat)

                # Set tile index
                index = atlas[origin]

                if index == 0:
                    output_tile_array[0, y, x] = np.array((0, 0))
                else:
                    output_tile_array[0, y, x] = np.array(
                        (index // 128 + 1, index % 128)
                    )

        layer[2] = output_tile_array

        # Collision
        colmaps = []
        for layer_i in block:
            colmaps.append(layers[layer_i][3])

        layer[3] = np.any(np.concatenate(colmaps, axis=0), axis=0)
        output.append(layer)

    return output


def resolve_resource_path(pth):
    resource_dirs = list(Path("").glob("resources/*/graphics"))
    for dir in resource_dirs:
        if (dir / pth).is_file():
            return dir / pth
    raise FileNotFoundError(pth)
