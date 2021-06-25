from PIL import Image
import numpy as np

from pathlib import Path


for p in Path("resources/graphics/particle_raw/").glob("*.png"):
    print(p)
    im = Image.open(p)
    in_array = np.array(im)
    arr = np.zeros((in_array.shape[0], in_array.shape[1], 4), dtype=in_array.dtype)

    if len(in_array.shape) > 2:
        in_array = in_array[:, :, 1]

    arr[:, :, 0] = in_array
    arr[:, :, 1] = in_array
    arr[:, :, 2] = in_array
    arr[:, :, 3] = in_array

    im_new = Image.fromarray(arr)

    im_new.save(Path("resources/graphics/particle_unused/") / p.name)
