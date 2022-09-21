import random
from tabnanny import verbose
from typing import Iterable
from ulivy.generator.pathfinder import Pathfinder
from ulivy.generator.ldtkcmanager import LdtkcManager
from pathlib import Path
import copy
import numpy as np
import time

ROOT = Path("world/world")
MULTIPLIER = 1000
WEIGHTS = True


class Tilechecker:
    """Object for various operations regarding elements and tile placing rules
    :param template_ndarrays -> A list of ndarrays with level tiles mapped onto them"""

    def __init__(
        self,
        template_ndarrays: list,
        elements: list,
        elements_col: list,
        non_place=[],
        log_weights=True,
        only_map=[],
        verbose=False,
    ):
        self.elements = elements
        self.elements_col = elements_col
        self.used_elements = set()
        self.verbose = verbose
        self.templates = [
            self.map_elements(x, y, skip_empty=True, add_new_elements=True)
            for x, y in template_ndarrays
        ]
        self.non_place_templates = [
            self.map_elements(x, y, skip_empty=True, add_new_elements=True)
            for x, y in non_place
        ]
        self.only_map_templates = [
            self.map_elements(x, y, skip_empty=True, add_new_elements=True)
            for x, y in only_map
        ]
        self.log_weights = log_weights
        self.allowed = self._build_rules()

    def _build_rules(self):
        """Builds the ruleset from the template. Keys and value inside a direction are element ids,
        which are the index of the item in self.elements. Also counts how many times what element was next to what element.
        eg. {0: {"North": {1, 2, 3}, "South": {5, 4, 9}}, 1: {"North": {}.....
        :return -> The ruleset"""
        timer = time.perf_counter()

        weights = {}

        n_ele = len(self.elements)
        allowed = np.zeros((4, n_ele, n_ele), dtype="?")

        # for template_ndarray in self.templates:
        for non_place, templates in (
            (False, self.templates),
            (True, self.non_place_templates),
        ):
            for arr in templates:
                hei, wid = arr.shape
                # Go through each tile and append all surrounding tiles to a dict
                # Also take a note of how many times an element was next to another, and on what side (for weights)
                for i, element in enumerate(np.nditer(arr)):
                    elem = int(element)
                    coords = [i // wid, i % wid]
                    for coord in self.coords_around(arr, coords):
                        y, x = coord
                        dr, dri = self.get_direction(coords, coord)
                        elem_id = arr[y][x]
                        if elem_id != -1:
                            if elem not in weights:
                                weights[elem] = {}
                            if dr not in weights[elem]:
                                weights[elem][dr] = {}
                            if elem_id not in weights[elem][dr]:
                                weights[elem][dr][elem_id] = 1

                            if not non_place:
                                self.used_elements.add(elem_id)
                            allowed[dri][elem][elem_id] = True
                            weights[elem][dr][elem_id] += 1

        # This will get explained to me later
        if self.log_weights:
            for from_elem in weights.keys():
                for dr in weights[from_elem].keys():
                    for k, v in weights[from_elem][dr].items():
                        weights[from_elem][dr][k] = np.log(v + 1)
        # Convert weights from number of occurences to a % chance
        for from_elem in weights.keys():
            for dr in weights[from_elem].keys():
                total = sum([v for v in weights[from_elem][dr].values()])
                for k, v in weights[from_elem][dr].items():
                    weights[from_elem][dr][k] = v / total

        # Set some more attributes
        self.weights = weights
        self.element_ids = {
            x for x in range(len(self.elements))
        }  # Used as a base of allowed element ids

        if self.verbose:
            print("Building the ruleset took:", time.perf_counter() - timer)
        return allowed

    def div_16(self, val):
        """Integer div val by 16. If val is iterable, integer div all values inside it by 16
        :param val -> item to divide by 16. If iterable, iterate over all items and create a list of all values // 16
        :return    -> val or val values // 16"""
        if isinstance(val, Iterable):
            return [x // 16 for x in val]
        return val // 16

    def get_direction(self, from_coords, to_coords):
        """Return the direction from from_coords to to_coords
        :param from_coords -> Coords to start from
        :param to_coords   -> Coords to end up to
        :return            -> Direction from from_coords to to_coords"""
        diff = [x[0] - x[1] for x in list(zip(from_coords, to_coords))]
        if diff[0] == 1:
            return "North", 0
        if diff[0] == -1:
            return "South", 1
        if diff[1] == 1:
            return "West", 2
        if diff[1] == -1:
            return "East", 3
        return False

    def coords_around(self, array, coords, steps=1):
        """Same as coords around, but return coords around 3 tiles away
        :param array  -> 2darray of the level youre working to fill
        :param coords -> a tuple of coords
        :param steps  -> How many steps away to return coordinates from
        :returns      -> A tuple of surrounding coord tuples: (y+steps,x), (y-steps,x), (y,x+steps), (y,x-steps)"""
        y, x = coords
        s = steps
        around = ((y, x + s), (y, x - s), (y + s, x), (y - s, x))
        # Remove coordinates with negative values
        around = tuple((i for i in around if i[0] >= 0 and i[1] >= 0))
        # Remove coordinates that exceed boundaries
        hei, wid = array.shape
        around = tuple((i for i in around if i[0] < hei and i[1] < wid))
        return around

    def cube_around(self, array, coords):
        """Return the coordinates around a given coordinate, with the corners also. Doesn't return out of bounds coordinates
        :param array  -> 2darray of the level youre working to fill
        :returns      -> A tuple of surrounding coord tuples: (y+1,x), (y-1,x), (y,x+1), (y,x-1)"""
        y, x = coords
        around = (
            (y, x + 1),
            (y, x - 1),
            (y + 1, x),
            (y - 1, x),
            (y - 1, x - 1),
            (y - 1, x + 1),
            (y + 1, x - 1),
            (y + 1, x + 1),
        )
        # Remove coordinates with negative values
        around = tuple((i for i in around if i[0] >= 0 and i[1] >= 0))
        # Remove coordinates that exceed boundaries
        hei, wid = array.shape
        around = tuple((i for i in around if i[0] < hei and i[1] < wid))
        return around

    def check_allowed(self, arr, poss, coords):
        """Check locations around a coordinate and return a set of element ids that are allowed in the coordinate
        :param arr      -> Numpy array of already decided elements
        :param poss     -> Numpy array of possibilities
        :param coords   -> A tuple of coords to check surroundings from (y, x)
        :return         -> A set of allowed element ids"""

        allowed = np.ones(len(self.elements), dtype="?")
        for coord in self.coords_around(arr, coords):
            _, dri = self.get_direction(coord, coords)

            allow = np.dot(poss[coord], self.allowed[dri])

            allowed = np.multiply(allowed, allow)

        return allowed

    def check_allowed_gemm(self, poss):
        """Updates the entire allowed matrix one iteration
        :param arr      -> Numpy array of already decided elements
        :param poss     -> Numpy array of possibilities
        :return         -> A set of allowed element ids"""

        r = np.dot(poss, self.allowed)

        new_poss = np.ones(poss.shape, dtype="?")

        new_poss[:-1] = np.multiply(new_poss[:-1], r[1:, :, 0])
        new_poss[1:] = np.multiply(new_poss[1:], r[:-1, :, 1])
        new_poss[:, :-1] = np.multiply(new_poss[:, :-1], r[:, 1:, 2])
        new_poss[:, 1:] = np.multiply(new_poss[:, 1:], r[:, :-1, 3])
        return new_poss

    def scan_elements(self, array, poss, single=False):
        """Brute force 'propagation' algorithm
        If a coordinates poss was changed, add that coordinates surroundings to the to-be-checked list. Repeat until list is exhausted
        :param array  -> Numpy array of already set elements
        :param poss     -> Numpy array of possibilities
        """
        while True:
            previous = np.copy(poss)
            poss = self.check_allowed_gemm(poss)

            for y in range(array.shape[0]):
                for x in range(array.shape[1]):
                    if array[y, x] > -1:
                        poss[y, x] = 0
                        poss[y, x][array[y, x]] = 1

            if single or np.all(poss == previous):
                break
        return poss

    def propagate_elements(self, array, poss, coords):
        """Process the influence of setting an element to the rest of the level.
        Add coords surrounding coordinates to a list, check their allowed tiles and update poss if needed.
        If a coordinates poss was changed, add that coordinates surroundings to the to-be-checked list. Repeat until list is exhausted
        :param array  -> Numpy array of already set elements
        :param poss   -> A dict of remaining coordinates' possible elements
        :param coords -> A tuple of coords from where to start the process
        """
        if isinstance(coords, list):
            propagations = [x for y in coords for x in self.coords_around(array, y)]
        else:
            propagations = [x for x in self.coords_around(array, coords)]
        while propagations:
            coords = propagations.pop(0)
            y, x = coords
            if np.sum(poss[y, x]) == 1:
                continue
            allowed = self.check_allowed(array, poss, coords)
            if np.all(poss[coords] == allowed):
                continue
            poss[coords] = allowed
            propagations.extend([x for x in self.coords_around(array, coords)])

    def map_elements(
        self, ndarray, ndarray_col, skip_empty=False, add_new_elements=False
    ):
        """Convert tiles in level to elements and map the ids to array
        :param ndarray                -> ndarray that has all level tile info
        :param skip_empty=False       -> Skip mapping elements of only 0s
        :param add_new_elements=False -> Add new elements into self.elements as they are found"""

        # Create a list of elements and map them to a 2darray
        depth, hei, wid = ndarray.shape
        array = np.full((hei, wid), -1, int)
        for x in range(wid):
            for y in range(hei):
                element = []
                element_col = []
                for d in range(depth):
                    element.append(ndarray[d][y][x])
                    if ndarray_col is not None:
                        element_col.append(ndarray_col[d][y][x])
                element = tuple(element)
                element_col = tuple(element_col)

                if skip_empty:
                    if sum(element) == 0:
                        continue

                if add_new_elements:
                    if element not in self.elements:
                        self.elements.append(element)
                        if ndarray_col is not None:
                            self.elements_col.append(element_col)

                if element not in self.elements:
                    raise IndexError(
                        f"Element {element} at coords ({y}, {x}) not found in elements!"
                    )

                array[y][x] = self.elements.index(element)
        return array

    def write_elements(self, level, array, ldtkc=False):
        """Write elements mapped in array to level
        :param level -> Target Level object to write to
        :param array -> Numpy array that contains the mapped elements"""
        hei, wid = array.shape

        # Go over the array and write each found element to the level
        if ldtkc:
            for y in range(hei):
                for x in range(wid):
                    element_id = array[y, x]
                    if element_id == -1:
                        continue
                    element = self.elements[element_id]
                    col = self.elements_col[element_id]
                    # For tile layer in the level
                    for i, layer in enumerate(
                        [x for x in level["layers"] if x[0] == "TILES"]
                    ):
                        # Apply collisions
                        layer[3][y, x] = col[i]

                        # And tiles
                        t = element[i]
                        layer = layer[2][0]

                        t_x = t // MULTIPLIER
                        t_y = t % MULTIPLIER
                        t_x += 1

                        layer[y, x][0] = t_x
                        layer[y, x][1] = t_y
            return level
            manager.write()
        else:
            tile_template = {
                "px": [128, 128],
                "src": [96, 16],
                "f": 0,
                "t": 14,
                "d": [136],
            }
            # Empty all layers
            for layer in level.layers.values():
                layer["gridTiles"] = []
            for y in range(hei):
                for x in range(wid):
                    element_id = array[y][x]
                    if element_id == -1:
                        continue

                    element = self.elements[element_id]
                    for i, layer in enumerate(level.layers.values()):
                        t = element[i]
                        if t == 0:
                            continue
                        tile = copy.deepcopy(tile_template)

                        tile["px"] = [int(x) * 16, int(y) * 16]
                        tile["d"] = [int(level.coordToInt((x, y), wid))]

                        tile["src"] = level.tToSrc(t)
                        tile["t"] = int(t)

                        layer["gridTiles"].append(tile)
            level.write()
        print("Wrote level")

    def get_weights(self, arr, from_coords, elements):
        """Calculate the weights for a selection from poss
        :param arr       -> Array containing the mapped elements
        :param selection -> A value selected from poss eg.((y, x), {1, 2, 3})
        :returns         -> A list of weights to be used in np.random.choice(..., p=)"""

        # If surrounding are still empty, return weights with all values valued the same
        if sum([arr[y, x] for y, x in self.coords_around(arr, from_coords)]) == -4:
            return elements / np.sum(elements)

        weights = elements.astype(float)
        for coords in self.coords_around(arr, from_coords):
            y, x = coords
            from_elem = arr[y][x]
            dr, _ = self.get_direction(coords, from_coords)
            for elem in range(len(weights)):
                if (
                    from_elem in self.weights
                    and dr in self.weights[from_elem]
                    and elem in self.weights[from_elem][dr]
                ):
                    weights[elem] *= self.weights[from_elem][dr][elem]
        # Weights doesnt always find the elements around it. In that case, dont handle this element right now
        # Not sure if this is correct behaviour
        total = np.sum(weights)
        if total == 0:
            return False
        weights = weights / total
        return weights


def create_ndarray(level, ldtkc=False):
    if ldtkc:
        tile_layers = [x for x in level["layers"] if x[0] == "TILES"]
        wid, hei = level["orig_dimensions"]
        depth = len(tile_layers)
        ndarray = np.zeros((depth, hei, wid), int)

        enum_size = level["layers"][0][3].shape[2]
        ndarray_coll = np.zeros((depth, hei, wid, enum_size), bool)

        for d, layer in enumerate(tile_layers):
            for y in range(hei):
                for x in range(wid):
                    t_x, t_y = layer[2][0, y, x]
                    if not t_x:
                        continue
                    t_x -= 1
                    tile_id = t_y + t_x * MULTIPLIER
                    ndarray[d][y][x] = tile_id
                    ndarray_coll[d, y, x] = layer[3][y, x]
        return ndarray, ndarray_coll

    wid, hei = [x // 16 for x in level.size]
    depth = len(level.layers)
    ndarray = np.zeros((depth, hei, wid), int)

    # Map all known tiles into an ndarray
    for d, layer in enumerate(level.layers.values()):
        for tile in layer["gridTiles"]:
            x, y = [a // 16 for a in tile["px"]]
            ndarray[d][y][x] = tile["t"]
    return ndarray, None


def convert_mapstring_to_key(mapstr):
    # Now also accepts integers
    mapstr = str(mapstr).strip()
    if mapstr[0] != "L":
        mapint = int(mapstr)
        if mapint < 1000:
            return 1000 * mapint
        return mapint
    if mapstr[-1] != "_":
        mapstr = mapstr + "_"
    id_e = [int(x[1:]) for x in mapstr.lower().split("_")[:-1]]
    return int(id_e[0] * 1000 + (len(id_e) > 1 and id_e[1] or 0))


def find_pois(arr, poi_template):
    hei, wid = arr.shape

    x_scan = np.zeros((hei, wid), int)
    for y in range(hei):
        for x, elem in enumerate(np.nditer(arr[y])):
            if elem != -1:
                x_scan[y, x] = x_scan[y, x - 1] + 1
            else:
                x_scan[y, x] = 0
    y_scan = np.zeros((hei, wid), int)
    for x in range(wid):
        for y in range(hei):
            elem = arr[y, x]
            if elem != -1:
                y_scan[y, x] = y_scan[y - 1, x] + 1
            else:
                y_scan[y, x] = 0
    composite = np.multiply(x_scan, y_scan)
    lvl_ents = [x for x in poi_template["entities"]]
    lvl_regs = [x for x in poi_template["regions"]]
    pois = []
    entities = []
    regions = []
    while np.sum(composite):
        bottom_right = np.unravel_index(np.argmax(composite), composite.shape)
        y, x = bottom_right
        hei, wid = y_scan[y, x], x_scan[y, x]
        top_left = tuple([y - hei + 1, x - wid + 1])
        slice = np.copy(arr[y - hei + 1 : y + 1, x - wid + 1 : x + 1])
        pois.append(slice)
        composite[y - hei + 1 : y + 1, x - wid + 1 : x + 1] = 0

        # Find out entities in the poi
        coords = []  # All coordinates inside the poi
        for y in range(y - hei + 1, y + 1):
            for x in range(x - wid + 1, x + 1):
                coords.append(tuple([x, y]))
        ents = {}
        for ent in lvl_ents:
            loc = tuple([a // 16 for a in ent["location"]])
            if loc in coords:
                x = loc[0] - top_left[1]
                y = loc[1] - top_left[0]
                ents[tuple([y, x])] = ent
        entities.append(ents)
        # Find out regions in the poi
        regs = {}
        for reg in lvl_regs:
            loc = tuple([a // 16 for a in reg["location"]])
            if loc in coords:
                x = loc[0] - top_left[1]
                y = loc[1] - top_left[0]
                regs[tuple([y, x])] = reg
        regions.append(regs)

    return pois, entities, regions


def place_pois(
    array,
    level,
    pois,
    entities,
    regions,
    amount,
):
    """Returns the center points of the placed down pois"""
    poi_centers = []
    portals_to_fix = {}
    pois = list(zip(pois, entities, regions))
    random.shuffle(pois)
    for poi, ent, reg in pois[:amount]:
        hei, wid = poi.shape
        opt = list(np.array(np.where(array == -1)).T)
        np.random.shuffle(opt)
        while opt:
            y, x = opt.pop(0)
            arr_slice = array[y - hei + 1 : y + 1, x - wid + 1 : x + 1]
            if list(np.unique(arr_slice)) == [-1]:
                array[y - hei + 1 : y + 1, x - wid + 1 : x + 1] = poi
                poi_centers.append((y - hei // 2, x - wid // 2))

                # And place entities also
                hei, wid = poi.shape
                top_left = tuple([y - hei + 1, x - wid + 1])
                if ent:
                    for k, v in ent.items():
                        x2 = (top_left[0] + k[0] + 0.5) * 16
                        y2 = (top_left[1] + k[1] + 0.5) * 16
                        v["location"] = [y2, x2]
                        level["entities"].append(v)
                # And place regions (portals) also
                if reg:
                    for k, v in reg.items():
                        x2 = (top_left[0] + k[0] + 0.5) * 16
                        y2 = (top_left[1] + k[1] + 0.5) * 16
                        v["location"] = [y2, x2]
                        level["regions"].append(v)

                        target_id = convert_mapstring_to_key(v["f_target_level"])
                        portals_to_fix[target_id] = [
                            top_left[1] + k[1],
                            top_left[0] + k[0],
                        ]
                break
    return poi_centers, portals_to_fix


def get_skins(arr):
    hei, wid = arr.shape

    x_scan = np.zeros((hei, wid), int)
    for y in range(hei):
        for x, elem in enumerate(np.nditer(arr[y])):
            if elem != -1:
                x_scan[y, x] = x_scan[y, x - 1] + 1
            else:
                x_scan[y, x] = 0
    y_scan = np.zeros((hei, wid), int)
    for x in range(wid):
        for y in range(hei):
            elem = arr[y, x]
            if elem != -1:
                y_scan[y, x] = y_scan[y - 1, x] + 1
            else:
                y_scan[y, x] = 0
    composite = np.multiply(x_scan, y_scan)
    skins = []
    while np.sum(composite):
        bottom_right = np.unravel_index(np.argmax(composite), composite.shape)
        y, x = bottom_right
        hei, wid = y_scan[y, x], x_scan[y, x]
        skins.append(((y, x), np.copy(arr[y - hei + 1 : y + 1, x - wid + 1 : x + 1])))
        composite[y - hei + 1 : y + 1, x - wid + 1 : x + 1] = 0
    skins.sort(key=lambda x: (x[0], x[1]))  # Sort by y then x, ascending
    skins_sorted = {}
    for skin in skins:
        coord, array = skin
        y, x = coord
        if y not in skins_sorted:
            skins_sorted[y] = []
        skins_sorted[y].append(array)
    return skins_sorted


def apply_skins(arr, skins):
    rng = np.random.default_rng()
    for bucket in skins.values():
        base = bucket[0]
        hei, wid = base.shape
        locations = find_subarrays(arr, base)
        skin_ids = rng.integers(0, len(bucket), len(locations))
        for i, skin_id in enumerate(skin_ids):
            if skin_id == 0:
                continue
            y, x = locations[i]
            arr[y : y + hei, x : x + wid] = bucket[skin_id]


def find_subarrays(a, b):
    shape = [n - m + 1 for n, m in zip(a.shape, b.shape)] + list(b.shape)
    strides = a.strides + a.strides
    view = np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    result = np.where(np.all(view == b, axis=(2, 3)))
    return np.array(result).T


def create_level(
    levels_data,
    target_id,
    template_id,
    road_id,
    poi_id,
    skin_id,
    mainroad_id,
    non_place_ids: list,
    path,
    poi_amount,
    ldtkc=True,
    verbose=False,
):
    """Parameters are file name strings for ldtk, level ids for ldtkc"""
    if not path:
        print("Please specify the path. eg. path=((27, 12), [(15, 64)])")
        raise Exception
    levels_to_overwrite = {}

    elements = []
    elements_col = []

    # For LDTKC map creation
    # manager = LdtkcManager("world.ldtkc")
    target = levels_data[target_id]
    template = levels_data[template_id]
    road_template = levels_data[road_id]
    poi_template = levels_data[poi_id]
    skin_template = levels_data[skin_id]
    mainroad_template = levels_data[mainroad_id]
    non_place_templates = [levels_data[x] for x in non_place_ids]

    templates = [create_ndarray(x, ldtkc=ldtkc) for x in [template]]
    non_place_templates = [
        create_ndarray(x, ldtkc=ldtkc)
        for x in [road_template, poi_template] + non_place_templates
    ]
    road_templates = [create_ndarray(x, ldtkc=ldtkc) for x in [road_template]]

    ndarray, ndarray_col = create_ndarray(target, ldtkc=ldtkc)

    checker = Tilechecker(
        templates,
        elements,
        elements_col,
        non_place=non_place_templates,
        only_map=[(ndarray, ndarray_col)],
        log_weights=True,
    )
    roads = Tilechecker(road_templates, elements, elements_col)

    ndarray, ndarray_col = create_ndarray(target, ldtkc=ldtkc)

    timer = time.perf_counter()

    # Map all targets pre-set elements to a 2darray
    if verbose:
        print("Elements in this level:", len(elements))
    arr = checker.map_elements(ndarray, ndarray_col, skip_empty=True)

    # Level dimensions
    hei, wid = arr.shape

    # Initialize poss with all coords having all options
    poss = np.zeros((hei, wid, len(checker.element_ids)), dtype="?")
    for elem_id in checker.used_elements:
        poss[:, :, elem_id] = 1

    # Update arr with information about pre-set elements
    for coords in list(zip(*np.nonzero(arr != -1))):
        y, x = coords
        elem_id = arr[y, x]
        poss[y, x] = 0
        poss[y, x, elem_id] = 1

    if verbose:
        print("Pre-set elements", time.perf_counter() - timer)

    # Create the path
    pathfinder = Pathfinder(checker)

    grass_element = roads.map_elements(*create_ndarray(road_template, ldtkc=ldtkc))[
        0, 0
    ]

    mainroad_arr = checker.map_elements(*create_ndarray(mainroad_template, ldtkc=ldtkc))

    mainroad = {}
    mainroad["hor"] = mainroad_arr[:, 0:2]
    mainroad["ver"] = mainroad_arr[:, 2:4]
    mainroad["ne"] = mainroad_arr[:, 4:6]
    mainroad["wn"] = mainroad_arr[:, 6:8]
    mainroad["se"] = mainroad_arr[:, 8:10]
    mainroad["ws"] = mainroad_arr[:, 10:12]

    path_start = tuple([x // 2 for x in path[0][0]])
    path_end = tuple([x // 2 for x in path[1][1]])
    road_path = pathfinder.create_road_path(arr, path[0][1], [path[1][0]])
    road_path = [path_start] + road_path + [path_end]
    path = []
    for pre, coord, post in zip(road_path, road_path[1:], road_path[2:]):
        pre_dir, _ = checker.get_direction(coord, pre)
        post_dir, _ = checker.get_direction(coord, post)
        if pre_dir in ("West", "East") and post_dir in ("West", "East"):
            dir = "hor"
        elif pre_dir in ("South", "North") and post_dir in ("South", "North"):
            dir = "ver"
        elif pre_dir in ("North", "East") and post_dir in ("North", "East"):
            dir = "ne"
        elif pre_dir in ("West", "North") and post_dir in ("West", "North"):
            dir = "wn"
        elif pre_dir in ("South", "East") and post_dir in ("South", "East"):
            dir = "se"
        elif pre_dir in ("West", "South") and post_dir in ("West", "South"):
            dir = "ws"

        y, x = coord[0] * 2, coord[1] * 2
        for y2, x2 in ((0, 0), (0, 1), (1, 0), (1, 1)):
            path.append((y + y2, x + x2))
            elem = mainroad[dir][y2, x2]
            arr[y + y2, x + x2] = elem
            poss[y + y2, x + x2] = 0
            poss[y + y2, x + x2, elem] = 1

    # Place down points of interest
    arr_no_poi = np.copy(arr)
    poi_ndarray, poi_col = create_ndarray(poi_template, ldtkc=ldtkc)
    poi_arr = checker.map_elements(
        poi_ndarray, poi_col, skip_empty=True, add_new_elements=True
    )
    pois, entities, regions = find_pois(poi_arr, poi_template)
    if not poi_amount:
        poi_amount = len(pois)
    centers, portals_to_fix = place_pois(
        arr, target, pois, entities, regions, poi_amount
    )

    # Create a grass path from all POIs to the main road
    for center in centers:
        poi_path = pathfinder.create_path(arr_no_poi, center, [path])
        for coord in poi_path:
            y, x = coord
            if arr[y, x] == -1:
                arr[y, x] = grass_element

    # Scan the whole level before we beging WFC
    poss = checker.scan_elements(arr, poss)

    arr_copy = np.copy(arr)
    poss_copy = np.copy(poss)
    finished = False
    while not finished:
        try:
            while -1 in arr:
                poss_sel = np.sum(poss, axis=2)
                if verbose:
                    print(f"{np.sum(poss_sel>1)} tiles left to fill")
                poss_sel[poss_sel < 2] = 999
                m = np.min(poss_sel)
                if m == 999:
                    if verbose:
                        print("Level out of options!")
                    break
                opt = np.array(np.where(poss_sel == m)).T

                y, x = opt[np.random.randint(len(opt))]

                if WEIGHTS:
                    if not (
                        weights := checker.get_weights(arr, (y, x), poss[y, x])
                    ).any():
                        continue
                    else:
                        weights = poss[y, x] / np.sum(poss[y, x])

                element_id = np.random.choice(list(checker.element_ids), p=weights)

                poss[y, x] = 0
                poss[y, x, element_id] = 1
                arr[y, x] = element_id

                checker.propagate_elements(arr, poss, (y, x))

            for y in range(hei):
                for x in range(wid):
                    if arr[y, x] == -1:
                        element_id = int(np.where(poss[y, x] == 1)[0])
                        poss[y, x] = 0
                        poss[y, x, element_id] = 1
                        arr[y, x] = element_id
            finished = True
        except TypeError:
            arr = np.copy(arr_copy)
            poss = np.copy(poss_copy)

    # Get the skins from the template and apply them
    skin_arr = checker.map_elements(
        *create_ndarray(skin_template, ldtkc=ldtkc),
        skip_empty=True,
        add_new_elements=True,
    )
    skins = get_skins(skin_arr)
    apply_skins(arr, skins)

    if verbose:
        print("Running time:", int(time.perf_counter() - timer), "s")
    # # Write elements mapped into arr to the target
    levels_to_overwrite[target_id] = checker.write_elements(target, arr, ldtkc=ldtkc)

    # And prepare data to fix portals from interiors
    for k, v in portals_to_fix.items():
        level = levels_data[k]
        level["regions"][0]["f_target_location"] = v
        levels_to_overwrite[k] = level

    return levels_to_overwrite
