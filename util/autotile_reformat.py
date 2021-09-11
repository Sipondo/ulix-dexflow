from pathlib import Path
import os
from PIL import Image, ImageFont
import numpy as np

p = Path("../resources/essentials/graphics/autotiles")

print(p.absolute())

for infile in p.glob("raw/*.png"):
    print(f"started file {infile.stem}")

    src_img = Image.open(infile).convert("RGBA")
    src_w, src_h = src_img.size

    img_w = src_h // 4 * 3
    img_h = src_h

    src_repeats = src_w // img_w

    for i in range(src_repeats):
        print(infile.stem, i)

        if src_repeats == 1:
            img = src_img.resize((48, 64), resample=Image.NEAREST)
        else:
            img = src_img.crop((img_w * i, 0, img_w * (i + 1), src_h)).resize(
                (48, 64), resample=Image.NEAREST
            )
        old_format = np.asarray(img)

        stupid_bits = old_format[:][0:16]

        normal_bits = old_format[:][16:]
        # normal_bits = (48, 48, 4)

        # normal bits arrangement
        top_left = normal_bits[:16, :16]
        top_center = normal_bits[:16, 16:32]
        top_right = normal_bits[:16, 32:48]
        mid_left = normal_bits[16:32, :16]
        mid_center = normal_bits[16:32, 16:32]
        mid_right = normal_bits[16:32, 32:48]
        bot_left = normal_bits[32:48, :16]
        bot_center = normal_bits[32:48, 16:32]
        bot_right = normal_bits[32:48, 32:48]

        # stupid_bits = (16, 48, 4)

        # stupid bits arrangement
        circle_top_left = stupid_bits[:8, :8]
        circle_top_right = stupid_bits[:8, 8:16]
        circle_bot_left = stupid_bits[8:16, :8]
        circle_bot_right = stupid_bits[8:16, 8:16]

        random_top_left = stupid_bits[:8, 32:40]
        random_top_right = stupid_bits[:8, 40:48]
        random_bot_left = stupid_bits[8:16, 32:40]
        random_bot_right = stupid_bits[8:16, 40:48]

        # new img
        formatted_img_array = np.zeros((112, 112, 4), dtype=np.uint8)
        # alpha = flat_img[3::4]
        # alpha[:] = 255
        # formatted_img_array = np.reshape(flat_img, (112, 112, 4))

        # single tile things
        single_tile_horizontal = top_center.copy()
        single_tile_horizontal[8:16, :] = bot_center[8:16, :]
        single_tile_left = single_tile_horizontal.copy()
        single_tile_left[:8, :8] = circle_top_left
        single_tile_left[8:16, :8] = circle_bot_left
        single_tile_right = single_tile_horizontal.copy()
        single_tile_right[:8, 8:16] = circle_top_right
        single_tile_right[8:16, 8:16] = circle_bot_right

        single_tile_vertical = mid_left.copy()
        single_tile_vertical[:, 8:16] = mid_right[:, 8:16]
        single_tile_top = single_tile_vertical.copy()
        single_tile_top[:8, :8] = circle_top_left
        single_tile_top[:8, 8:16] = circle_top_right
        single_tile_bot = single_tile_vertical.copy()
        single_tile_bot[8:16, :8] = circle_bot_left
        single_tile_bot[8:16, 8:16] = circle_bot_right

        # normal tiles
        formatted_img_array[16:32, 16:32] = top_left
        formatted_img_array[16:32, 32:48] = top_right
        formatted_img_array[16:32, 48:64] = top_center
        formatted_img_array[32:48, 16:32] = bot_left
        formatted_img_array[32:48, 32:48] = bot_right
        formatted_img_array[32:48, 48:64] = bot_center
        formatted_img_array[48:64, 16:32] = mid_left
        formatted_img_array[48:64, 32:48] = mid_right
        formatted_img_array[48:64, 48:64] = mid_center

        # single tiles
        formatted_img_array[:16, 16:32] = single_tile_left
        formatted_img_array[:16, 32:48] = single_tile_right
        formatted_img_array[:16, 48:64] = single_tile_horizontal
        formatted_img_array[16:32, :16] = single_tile_top
        formatted_img_array[32:48, :16] = single_tile_bot
        formatted_img_array[48:64, :16] = single_tile_vertical

        # round tile
        formatted_img_array[48:64, 64:80] = stupid_bits[:16, :16]

        # unusual tiles
        big_tile = np.tile(mid_center, (3, 3, 1))
        formatted_img_array[0:48, 64:112] = big_tile
        formatted_img_array[8:16, 72:80] = random_bot_right
        formatted_img_array[16:24, 72:80] = random_top_right
        formatted_img_array[8:16, 80:88] = random_bot_left
        formatted_img_array[16:24, 80:88] = random_top_left
        formatted_img_array[8:16, 96:104] = random_bot_left
        formatted_img_array[16:24, 96:104] = random_top_left
        formatted_img_array[8:16, 104:112] = random_bot_right
        formatted_img_array[16:24, 104:112] = random_top_right
        formatted_img_array[32:40, 72:80] = random_top_right
        formatted_img_array[32:40, 80:88] = random_top_left
        formatted_img_array[32:40, 96:104] = random_top_left
        formatted_img_array[32:40, 104:112] = random_top_right
        formatted_img_array[40:48, 72:80] = random_bot_right
        formatted_img_array[40:48, 80:88] = random_bot_left
        formatted_img_array[40:48, 96:104] = random_bot_left
        formatted_img_array[40:48, 104:112] = random_bot_right

        # other shapes
        big_tile = np.tile(mid_left, (2, 1, 1))
        formatted_img_array[48:80, 80:96] = big_tile
        big_tile = np.tile(mid_right, (2, 1, 1))
        formatted_img_array[48:80, 96:112] = big_tile
        formatted_img_array[56:64, 88:96] = random_bot_right
        formatted_img_array[64:72, 88:96] = random_top_right
        formatted_img_array[56:64, 96:104] = random_bot_left
        formatted_img_array[64:72, 96:104] = random_top_left

        big_tile = np.tile(top_center, (1, 2, 1))
        formatted_img_array[64:80, 48:80] = big_tile
        big_tile = np.tile(bot_center, (1, 2, 1))
        formatted_img_array[80:96, 48:80] = big_tile
        formatted_img_array[72:80, 56:64] = random_bot_right
        formatted_img_array[80:88, 56:64] = random_top_right
        formatted_img_array[72:80, 64:72] = random_bot_left
        formatted_img_array[80:88, 64:72] = random_top_left

        big_tile = np.tile(mid_center, (2, 2, 1))
        formatted_img_array[80:112, 80:112] = big_tile
        formatted_img_array[88:104, 88:104] = formatted_img_array[56:72, 88:104]
        formatted_img_array[88:104, 80:88] = formatted_img_array[56:72, 96:104]
        formatted_img_array[88:104, 104:112] = formatted_img_array[56:72, 88:96]
        formatted_img_array[80:88, 88:104] = formatted_img_array[64:72, 88:104]
        formatted_img_array[104:112, 88:104] = formatted_img_array[56:64, 88:104]

        big_tile = np.tile(mid_center, (1, 2, 1))
        formatted_img_array[96:112, 48:80] = big_tile

        formatted_img_array[104:112, 56:72] = formatted_img_array[56:64, 88:104]
        formatted_img_array[96:104, 48:56] = random_top_left
        formatted_img_array[96:104, 72:80] = random_top_right

        # all shapes already exist, so copy some stuff

        formatted_img_array[64:96, :32] = formatted_img_array[16:48, 16:48]
        formatted_img_array[72:88, 8:24] = formatted_img_array[56:72, 88:104]
        formatted_img_array[96:112, :16] = mid_left
        formatted_img_array[96:112, 16:32] = mid_right
        formatted_img_array[96:104, 8:24] = formatted_img_array[64:72, 88:104]
        formatted_img_array[104:112, 8:24] = formatted_img_array[56:64, 88:104]

        formatted_img_array[64:80, 32:48] = top_center
        formatted_img_array[80:96, 32:48] = bot_center
        formatted_img_array[72:88, 32:40] = formatted_img_array[8:24, 96:104]
        formatted_img_array[72:88, 40:48] = formatted_img_array[8:24, 104:112]
        formatted_img_array[96:112, 32:48] = formatted_img_array[32:48, 96:112]

        test = Image.fromarray(formatted_img_array)

        if src_repeats == 1:
            test.save(p / f"{infile.stem}.png")
        else:
            (p / f"slide/{infile.stem}").mkdir(parents=True, exist_ok=True)
            test.save(p / f"slide/{infile.stem}/{infile.stem}_slide_{i}_{500}.png")

        print(f"finished file {infile.stem}")

