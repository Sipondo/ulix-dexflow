import json
import math
import numpy as np
from io import BytesIO
from pathlib import Path

from game.helpers.ldtkjson import ldtk_json_from_dict
from game.upl.uplmanager import UplParser


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
            n: [
                x["enumValueId"] for x in t.enum_tags if n in x["tileIds"]
            ]  # .replace("X", "ESWN")
            for n in range(t.px_hei * t.px_wid // 256)
        }
        for t in a.defs.tilesets
    }

    customData = {t.uid: t.custom_data for t in a.defs.tilesets}

    enumValues = list(
        dict.fromkeys(
            ["E", "S", "W", "N", "X"]
            + [x["enumValueId"] for t in a.defs.tilesets for x in t.enum_tags]
        )
    )[5:]

    for enum in [x for x in a.defs.enums if x.identifier in ("Settables")]:
        settables = [x.id.lower() for x in enum.values]

    for enum in [x for x in a.defs.enums if x.identifier in ("Switches")]:
        switches = [x.id.lower() for x in enum.values]

    print("ENUMVALUES:", enumValues)
    print("CUSTOMDATA:", customData)
    print("SETTABLES:", settables)
    print("SWITCHES:", switches)

    for level in a.levels:
        print("\n", "-" * 50, f"LEVEL: {level.identifier}", "-" * 50)
        # print({field.identifier: field.value for field in level.field_instances})

        id_e = [int(x[1:]) for x in level.identifier.lower().split("_")[:-1]]
        id = str(id_e[0] * 1000 + (len(id_e) > 1 and id_e[1] or 0))

        last_layer = "init"
        depth = 0
        layer_depths = []
        for layer in level.layer_instances:
            if "Boundaries" in layer.identifier:
                continue
            # if layer.type == "IntGrid":
            #     continue
            if last_layer != "init" and last_layer != layer.tileset_rel_path:
                layer_depths.append(depth)
                depth = 0
            depth += 1
            last_layer = layer.tileset_rel_path
        layer_depths.append(depth)
        print(layer_depths)

        # TODO: fix renderer so it doesn't require 16x16 worlds
        orig_width = level.px_wid // 16
        orig_height = level.px_hei // 16
        width = math.ceil(level.px_wid / 256 + 1) * 16
        height = math.ceil(level.px_hei / 256 + 1) * 16

        # width = math.ceil(level.px_wid / 16 + 1)
        # height = math.ceil(level.px_hei / 16 + 1)

        # TODO: get rid of this hack as well (2^ maps)
        width = 2 ** math.ceil(math.log2(width))
        height = 2 ** math.ceil(math.log2(height))

        entity_array = None
        reversed_instances = [
            x
            for x in reversed(level.layer_instances)
            if "Boundaries" not in x.identifier
        ]

        current_layer = 0
        entity_height = 0
        output_layers = []

        for index, depth_block in enumerate(reversed(layer_depths)):
            print("Depth Block:", depth_block)
            curinst = reversed_instances[current_layer]
            # if curinst.tileset_rel_path:
            #     print(
            #         "\n\nParents:",
            #         [
            #             x.stem
            #             for x in list(Path(curinst.tileset_rel_path).parents)[::-1]
            #             if "graphics" in str(x)
            #         ],
            #         "\n\n",
            #     )
            tileset = (
                curinst.tileset_rel_path
                and "/".join(
                    [
                        x.stem
                        for x in list(Path(curinst.tileset_rel_path).parents)[::-1]
                        if "graphics" in str(x)
                    ][1:]
                    + [Path(curinst.tileset_rel_path).stem]
                )
                # f"{Path(curinst.tileset_rel_path).parent.stem}/{Path(curinst.tileset_rel_path).stem}"
            )

            if tileset != None:
                tile_array = np.zeros(
                    (depth_block, height, width, 2), dtype=np.dtype("uint16")
                )
                col_array = np.zeros(
                    (depth_block, height, width, 9), dtype=np.dtype("bool")
                )
                for current_depth in range(depth_block):
                    layer = reversed_instances[current_layer]
                    print(
                        f"{layer.identifier: <20} - {layer.type: <10} - {layer.tileset_rel_path}"
                    )

                    if layer.type == "Tiles":
                        for tile in layer.grid_tiles:
                            # if coldefs[layer.tileset_def_uid][tile.t]:
                            #     print(vars(tile), layer.identifier, coldefs[layer.tileset_def_uid][tile.t])

                            loc = (tile.px[0] // 16, tile.px[1] // 16)
                            tile_array[current_depth, loc[1], loc[0]] = (
                                tile.src[0] // 16 + 1,
                                tile.src[1] // 16,
                            )
                            col_array[current_depth, loc[1], loc[0]] = coldef_to_bool(
                                coldefs[layer.tileset_def_uid][tile.t]
                            )
                    if layer.type == "IntGrid":
                        for tile in layer.auto_layer_tiles:
                            loc = (
                                tile.px[0] // 16,
                                tile.px[1] // 16,
                            )
                            tile_array[current_depth, loc[1], loc[0]] = (
                                tile.src[0] // 16 + (tile.f % 2) + 1,
                                tile.src[1] // 16 + (tile.f // 2),
                            )
                            col_array[current_depth, loc[1], loc[0]] = coldef_to_bool(
                                coldefs[layer.tileset_def_uid][tile.t]
                            )
                    current_layer += 1
                colmap = col_array[0]
                for individual in col_array[1:]:
                    colmap = colmap | individual

                # # Collision out of bounds
                # colmap = (
                #     colmap
                #     | np.repeat(
                #         np.expand_dims(np.sum(np.sum(tile_array, axis=3), axis=0), axis=2),
                #         4,
                #         axis=2,
                #     )
                #     < 1
                # )

                output_layers.append(["TILES", tileset, tile_array, colmap])
            else:
                print(
                    "IDENTIFIER", reversed_instances[current_layer].identifier.lower()
                )
                # if reversed_instances[current_layer].identifier == "Entities_A":  # Type
                #     player_height = index
                if "Regions" in curinst.identifier:
                    output_layers.append(["REGIONS"])
                else:
                    output_layers.append(["ENTITIES", entity_height])
                    entity_height += 1
                current_layer += 1

        entities = []
        regions = []

        entity_height = 0
        for instance in reversed_instances:
            if instance.type == "Entities":
                if "Regions" in instance.identifier:
                    print(f"Regions: {instance.identifier}")
                    for raw_ent in instance.entity_instances:
                        entity = {}
                        entity["identifier"] = raw_ent.identifier
                        entity["location"] = raw_ent.px
                        for field in raw_ent.field_instances:
                            if ent_field_upl[raw_ent.def_uid][field.def_uid]:
                                entity[f"f_{field.identifier}"] = parser.parse(
                                    field.value
                                )
                                # print(entity[f"f_{field.identifier}"].pretty())
                            else:
                                entity[f"f_{field.identifier}"] = field.value
                        entity["width"] = raw_ent.width
                        entity["height"] = raw_ent.height
                        regions.append(entity)
                else:
                    print(f"Entities: {instance.identifier}")
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
                                    # print(entity[f"f_{field.identifier}"].pretty())
                            else:
                                entity[f"f_{field.identifier}"] = field.value
                        entity["width"] = raw_ent.width
                        entity["height"] = raw_ent.height
                        entity["layer"] = entity_height
                        entities.append(entity)
                    entity_height += 1

        all_level_data[id] = {
            "layers": output_layers,
            "p_height": 0,
            "entities": entities,
            "regions": regions,
            "fields": {
                field.identifier: field.value for field in level.field_instances
            },
            "orig_dimensions": (orig_width, orig_height),
        }

        # print("Total tilesets:", [x[0] for x in output_layers])
        # print(
        #     "Total shapes:",
        #     [x[2].shape if x[0] == "TILES" else x for x in output_layers],
        # )
        # print("Player height:", 0)
        # print("Entities", entities)
        # print("Regions:", "\n\n".join([str(x) for x in regions]))
        # print("\n\n\n")

    world_data = {}

    world_data["levels"] = all_level_data
    world_data["world"] = {
        "enumValues": enumValues,
        "settables": settables,
        "switches": switches,
    }

    f = BytesIO()
    np.savez_compressed(f, **world_data)
    f.seek(0)
    out = f.read()

    with open("world.ldtkc", "wb") as file:
        file.write(out)
