"""
Fatlas
=====

Fatlas is a class for managing textures atlases: packing multiple texture into
one. With it, you are reducing the number of image to load and speedup the
application loading.

The Fatlas class is identical to an Atlas other than that it stores the
original image as texture and does not split the texture into smaller parts.
The indices are available instead of the subtextures. This allows the shader
to crop the desired area reducing the amount of textures required on the GPU.

"""

__all__ = ("Fatlas",)

import json
from os.path import basename, dirname, join, splitext
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import AliasProperty, DictProperty, ListProperty
import os


# late import to prevent recursion
CoreImage = None


class Fatlas(EventDispatcher):
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
        super(Fatlas, self).__init__()
        self._load()

    def __getitem__(self, key):
        return self.textures[key]

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
            self.ids[k] = [float(v[0]), 4096.0 - v[1] - v[3], float(v[2]), float(v[3])]

