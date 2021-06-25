# from midi2audio import FluidSynth
from pathlib import Path
from PIL import Image, ImageFont

# pth = Path("") / "../resources/audio/BGM/"

# print(pth.absolute())
# fs = FluidSynth(r"resources\audio\soundfont.sf2")
# # fs.midi_to_audio(pth, "output.flac")

# for infile in pth.glob("*.mid"):
#     fs.midi_to_audio(infile, pth / f"{infile.stem}.flac")

ESSENTIALS_DIR = Path("..")

p = ESSENTIALS_DIR / "Graphics/Tilesets"

p_to = Path("resources/essentials/graphics/tilesets")

for infile in p.glob("*.png"):
    print(infile)
    img = Image.open(infile)
    size = 0.5
    img = img.resize(
        (int(img.size[0] * size), int(img.size[1] * size)), resample=Image.NEAREST
    )
    img_new = Image.new(img.mode, (img.size[0], img.size[1] + 16))
    img_new.paste(img, (0, 16, img.size[0], img.size[1] + 16))
    img_new.save(p_to / f"{infile.stem}.png".lower())

p = ESSENTIALS_DIR / "Graphics/Autotiles"

p_to = Path("resources/essentails/graphics/autotiles")

for infile in p.glob("*.png"):
    print(infile)
    img = Image.open(infile)
    # size = 0.5
    # img = img.resize(
    #     (int(img.size[0] * size), int(img.size[1] * size)), resample=Image.NEAREST
    # )
    img.save(p_to / f"{infile.stem}.png".lower())

