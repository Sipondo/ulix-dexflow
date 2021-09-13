from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
import pandas as pd
from math import *

p = Path("../resources/essentials/graphics/items")

df = pd.read_csv(Path("../resources/essentials/PBS/items.csv"), index_col=0, skiprows=1)
width = 40
height = ceil(len(df) / 40)


canvas = Image.new("RGBA", (width * 24, height * 24), "#00000000")
draw = ImageDraw.Draw(canvas)

skipped = 0
for i, row in df.iterrows():
    try:
        i = int(i) - 1 - skipped
        img = (
            Image.open(p / f"{str(row[0]).lower().replace(' ', '')}.png")
            .convert("RGBA")
            .resize((24, 24), resample=Image.NEAREST)
        )
        canvas.alpha_composite(img, ((i % 40) * 24, (i // 40) * 24))
    except Exception as e:
        if "#" not in str(i):
            skipped += 1
        continue

canvas.save(Path("../world/editor_helpers/item_ldtk_list.png"))
