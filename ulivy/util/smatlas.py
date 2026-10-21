"""
Smatlas
=====

Smatlas is a class for managing textures atlases: packing multiple texture into
one. With it, you are reducing the number of image to load and speedup the
application loading.

The Smatlas class is identical to an Atlas other than that it stores the
original image as texture and does not split the texture into smaller parts.
The indices are available instead of the subtextures. This allows the shader
to crop the desired area reducing the amount of textures required on the GPU.

"""

__all__ = ("Smatlas",)

import json
import numpy as np
from math import ceil, sqrt
from os.path import basename, dirname, join, splitext
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import AliasProperty, DictProperty, ListProperty
import os


# late import to prevent recursion
CoreImage = None


class Smatlas(EventDispatcher):
    """Manage texture atlas. See module documentation for more information.
    """

    original_textures = ListProperty([])
    """List of original atlas textures (which contain the :attr:`textures`).

    :attr:`original_textures` is a :class:`~kivy.properties.ListProperty` and
    defaults to [].

    .. versionadded:: 1.9.1
    """

    ids = DictProperty({})
    """List of available textures within the atla by ids.

    :attr:`ids` is a :class:`~kivy.properties.DictProperty` and defaults
    to {}.
    """

    def _get_filename(self):
        return self._filename

    filename = AliasProperty(_get_filename, None)
    """Filename of the current Atlas.

    :attr:`filename` is an :class:`~kivy.properties.AliasProperty` and defaults
    to None.
    """

    def __init__(self, filename):
        self._filename = filename
        super(Smatlas, self).__init__()
        self._load()

    def __getitem__(self, key):
        return self.ids[key]

    def _load(self):
        # late import to prevent recursive import.
        global CoreImage
        if CoreImage is None:
            from kivy.core.image import Image as CoreImage

        # must be a name finished by .atlas ?
        filename = self._filename
        assert filename.endswith(".atlas")
        filename = filename.replace("/", os.sep)

        Logger.debug("Atlas: Load <%s>" % filename)
        with open(filename, "r") as fd:
            meta = json.load(fd)

        Logger.debug("Atlas: Need to load %d images" % len(meta))
        d = dirname(filename)

        for subfilename, ids in meta.items():
            subfilename = join(d, subfilename)
            Logger.debug("Atlas: Load <%s>" % subfilename)

            # load the image
            ci = CoreImage(subfilename)
            atlas_texture = ci.texture
            atlas_texture.mag_filter = "nearest"
            self.original_textures.append(atlas_texture)

            self.ids.update(ids)

        for k, v in self.ids.items():
            x, y, square, l, imw, hs = v
            self.ids[k] = [
                float(x),
                float(y),
                float(square),
                float(l),
                float(imw),
                float(hs),
            ]

    @staticmethod
    def create(outname, filenames, size, padding=2, use_path=False):
        """This method can be used to create an atlas manually from a set of
        images.
        :Parameters:
            `outname`: str
                Basename to use for ``.atlas`` creation and ``-<idx>.png``
                associated images.
            `filenames`: list
                List of filenames to put in the atlas.
            `size`: int or list (width, height)
                Size of the atlas image. If the size is not large enough to
                fit all of the source images, more atlas images will created
                as required.
            `padding`: int, defaults to 2
                Padding to put around each image.
                Be careful. If you're using a padding < 2, you might have
                issues with the borders of the images. Because of the OpenGL
                linearization, it might use the pixels of the adjacent image.
                If you're using a padding >= 2, we'll automatically generate a
                "border" of 1px around your image. If you look at
                the result, don't be scared if the image inside is not
                exactly the same as yours :).
            `use_path`: bool, defaults to False
                If True, the relative path of the source png
                file names will be included in the atlas ids rather
                that just in the file names. Leading dots and slashes will be
                excluded and all other slashes in the path will be replaced
                with underscores. For example, if `use_path` is False
                (the default) and the file name is
                ``../data/tiles/green_grass.png``, the id will be
                ``green_grass``. If `use_path` is True, it will be
                ``data_tiles_green_grass``.
            .. versionchanged:: 1.8.0
                Parameter use_path added
        """
        # Thanks to
        # omnisaurusgames.com/2011/06/texture-atlas-generation-using-python/
        # for its initial implementation.
        try:
            from PIL import Image
        except ImportError:
            Logger.critical("Smatlas: Imaging/PIL are missing")
            raise

        # SIZE OVERWRITE 8192 x 8192
        size = (8192, 8192)

        if isinstance(size, (tuple, list)):
            size_w, size_h = list(map(int, size))
        else:
            size_w = size_h = int(size)

        # open all of the images
        ims = list()
        for f in filenames:
            fp = open(f, "rb")
            im = Image.open(fp)
            im.load()
            fp.close()

            # Reshape the spriteset
            w, h = im.size
            square = h
            length = w // square
            im_w = ceil(sqrt(length))
            im_h = ceil(w // square / im_w)

            im_re = Image.new("RGBA", (im_w * square, im_h * square))

            for i in range(length):
                x = i % im_w
                y = i // im_w

                tile = im.crop((i * square, 0, (i + 1) * square, square))

                im_re.paste(tile, (x * square, y * square), tile)

            print(f)

            # Calculate height offset

            a = np.flip(im, axis=0)

            b = a[:, : a.shape[0], 3]
            s = np.amax((b > 250), axis=0)
            height = np.amin((b[:, s] > 250).argmax(axis=0))
            height_share = (a.shape[0] - height) / a.shape[0]

            ims.append((f, im_re, h, length, im_w, height_share))

        # sort by image area
        ims = sorted(ims, key=lambda im: im[1].size[0] * im[1].size[1], reverse=True)

        # free boxes are empty space in our output image set
        # the freebox tuple format is: outidx, x, y, w, h
        freeboxes = [(0, 0, 0, size_w, size_h)]
        numoutimages = 1

        # full boxes are areas where we have placed images in the atlas
        # the full box tuple format is: image, outidx, x, y, w, h, filename
        fullboxes = []

        # do the actual atlasing by sticking the largest images we can
        # have into the smallest valid free boxes
        for imageinfo in ims:
            im = imageinfo[1]
            imw, imh = im.size
            imw += padding
            imh += padding
            if imw > size_w or imh > size_h:
                Logger.error(
                    "Atlas: image %s (%d by %d) is larger than the atlas size!"
                    % (imageinfo[0], imw, imh)
                )
                return

            inserted = False
            while not inserted:
                for idx, fb in enumerate(freeboxes):
                    # find the smallest free box that will contain this image
                    if fb[3] >= imw and fb[4] >= imh:
                        # we found a valid spot! Remove the current
                        # freebox, and split the leftover space into (up to)
                        # two new freeboxes
                        del freeboxes[idx]
                        if fb[3] > imw:
                            freeboxes.append(
                                (fb[0], fb[1] + imw, fb[2], fb[3] - imw, imh)
                            )

                        if fb[4] > imh:
                            freeboxes.append(
                                (fb[0], fb[1], fb[2] + imh, fb[3], fb[4] - imh)
                            )

                        # keep this sorted!
                        freeboxes = sorted(freeboxes, key=lambda fb: fb[3] * fb[4])
                        fullboxes.append(
                            (
                                im,
                                fb[0],
                                fb[1] + padding,
                                fb[2] + padding,
                                imw - padding,
                                imh - padding,
                                imageinfo[0],
                                imageinfo[2],
                                imageinfo[3],
                                imageinfo[4],
                                imageinfo[5],
                            )
                        )
                        inserted = True
                        break

                if not inserted:
                    # oh crap - there isn't room in any of our free
                    # boxes, so we have to add a new output image
                    freeboxes.append((numoutimages, 0, 0, size_w, size_h))
                    numoutimages += 1

        # now that we've figured out where everything goes, make the output
        # images and blit the source images to the appropriate locations
        Logger.info("Atlas: create an {0}x{1} rgba image".format(size_w, size_h))
        outimages = [
            Image.new("RGBA", (size_w, size_h)) for i in range(0, int(numoutimages))
        ]
        for fb in fullboxes:
            x, y = fb[2], fb[3]
            out = outimages[fb[1]]
            out.paste(fb[0], (fb[2], fb[3]))
            w, h = fb[0].size
            if padding > 1:
                out.paste(fb[0].crop((0, 0, w, 1)), (x, y - 1))
                out.paste(fb[0].crop((0, h - 1, w, h)), (x, y + h))
                out.paste(fb[0].crop((0, 0, 1, h)), (x - 1, y))
                out.paste(fb[0].crop((w - 1, 0, w, h)), (x + w, y))

        # save the output images
        for idx, outimage in enumerate(outimages):
            outimage.save("%s-%d.png" % (outname, idx))

        # write out an json file that says where everything ended up
        meta = {}
        for fb in fullboxes:
            fn = "%s-%d.png" % (basename(outname), fb[1])
            if fn not in meta:
                d = meta[fn] = {}
            else:
                d = meta[fn]

            # fb[6] contain the filename
            if use_path:
                # use the path with separators replaced by _
                # example '../data/tiles/green_grass.png' becomes
                # 'data_tiles_green_grass'
                uid = splitext(fb[6])[0]
                # remove leading dots and slashes
                uid = uid.lstrip("./\\")
                # replace remaining slashes with _
                uid = uid.replace("/", "_").replace("\\", "_")
            else:
                # for example, '../data/tiles/green_grass.png'
                # just get only 'green_grass' as the uniq id.
                uid = splitext(basename(fb[6]))[0]

            x, y, w, h, _, square, l, imw, hs = fb[2:11]
            d[uid] = x, y, square, l, imw, hs

        outfn = "%s.atlas" % outname
        with open(outfn, "w") as fd:
            json.dump(meta, fd)

        return outfn, meta


if __name__ == "__main__":
    """ Main line program. Process command line arguments
    to make a new atlas. """

    import sys
    from glob import glob

    argv = sys.argv[1:]
    # earlier import of kivy has already called getopt to remove kivy system
    # arguments from this line. That is all arguments up to the first '--'
    if len(argv) < 3:
        print(
            "Usage: python -m kivy.atlas [-- [--use-path] "
            "[--padding=2]] <outname> "
            "<size|512x256> <img1.png> [<img2.png>, ...]"
        )
        sys.exit(1)

    options = {"use_path": True}
    while True:
        option = argv[0]
        if option == "--use-path":
            options["use_path"] = True
        elif option.startswith("--padding="):
            options["padding"] = int(option.split("=", 1)[-1])
        elif option[:2] == "--":
            print("Unknown option {}".format(option))
            sys.exit(1)
        else:
            break
        argv = argv[1:]

    outname = argv[0]
    try:
        if "x" in argv[1]:
            size = list(map(int, argv[1].split("x", 1)))
        else:
            size = int(argv[1])
    except ValueError:
        print("Error: size must be an integer or <integer>x<integer>")
        sys.exit(1)

    filenames = [fname for fnames in argv[2:] for fname in glob(fnames)]
    ret = Smatlas.create(outname, filenames, size, **options)
    if not ret:
        print("Error while creating atlas!")
        sys.exit(1)

    fn, meta = ret
    print("Smatlas created at", fn)
    print(
        "%d image%s been created" % (len(meta), "s have" if len(meta) > 1 else " has")
    )

