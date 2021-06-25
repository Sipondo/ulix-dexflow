from pathlib import Path
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import pandas as pd
from math import *

p = Path("resources/graphics/Pokemon/Icons")

df = pd.read_csv(Path("resources/PBS/compressed/pokemon.csv"), index_col=0)
width = 64
height = ceil(len(df) / 64)


canvas = Image.new("RGBA", (width, height), "#00000000")
draw = ImageDraw.Draw(canvas)

for i, row in df.iterrows():
    try:
        img = (
            Image.open(p / f"{row.internalname}.png")
            .convert("RGBA")
            .resize((64, 32), resample=Image.NEAREST)
            .crop((0, 0, 32, 32))
        )
        canvas.alpha_composite(img, ((i % 64) * 32, (i // 64) * 32))
    except Exception as e:
        continue

canvas.save(Path("resources/graphics/generated/battler_ldtk_list.png"))


# for pth in p.glob("*.png"):
#     img = (
#         Image.open(pth)
#         .convert("RGBA")
#         .resize((64, 32), resample=Image.NEAREST)
#         .crop((0, 0, 32, 32))
#     )
