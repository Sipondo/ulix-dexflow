from tabnanny import verbose
import time
import copy
import random
from typing import final
import numpy as np


class Pathfinder:
    def __init__(self, tilechecker, verbose=False):
        self.checker = tilechecker
        self.verbose = verbose

    def end_close_enough(self, coords, end):
        y, x = coords  # Coords y and x
        e_y, e_x = end  # End loc y and x
        if x == e_x and abs(y - e_y) < 3:
            return True
        if y == e_y and abs(x - e_x) < 3:
            return True
        return False

    def next_to_path(self, arr, path, coord):
        for coords in self.checker.coords_around(arr, coord):
            if coords in path:
                return True

    def reduce_axis(self, b):
        b2 = b.reshape(*b.shape[:-2], -1, 2, b.shape[-1])
        idx = np.argmax(b2.sum(axis=-1), axis=-1)
        c = b2[np.arange(b2.shape[0]), idx]
        return c

    def find_road_path(self, arr, from_coords, to_coords: list):
        """Dijkstras pathfinding algo that moves in steps of 3.
        First goes from A to B, then from the middle of the just created path to C and so on....
        :param arr -> The array with mapped elements
        :param from_coords -> A tuple of coordinates to start from
        :param to_coords   -> A list of tuples of coordinates to coordinate to"""

        # arr = arr != -1
        # arr = self.reduce_axis(self.reduce_axis(arr).T).T

        final_path = []
        # from_coords = y, x = tuple([x // 2 for x in from_coords])
        for end_coord in to_coords:
            # end_coord = tuple([x // 2 for x in end_coord])
            visited = set()
            # First iteration draw a straight path. The ones after that start from the middle of the current known path
            if final_path:
                current = final_path[len(final_path) // 2]
            else:
                current = from_coords
            path = {current: [current]}
            while current:
                for coord in self.checker.coords_around(arr, current):
                    y, x = coord
                    dist = len(path[current]) + 1
                    if coord not in path or dist < len(path[coord]):
                        path[coord] = path[current] + [coord]

                visited.add(current)
                if isinstance(end_coord, set):
                    if self.next_to_path(arr, end_coord, current):
                        final_path.extend(path[current])
                        break
                else:
                    if current == end_coord:
                        final_path.extend(path[current])
                        break
                    # If under 3 tiles away in on direction from the end, add current path + end coord to the final path
                    # fill_path will fill the skipped coordinates
                    # if self.end_close_enough(current, end_coord):
                    #     final_path.extend(path[current] + [end_coord])
                    #     break
                next = None
                for c, p in path.items():
                    y, x = c
                    if arr[y][x]:
                        continue
                    if c in visited:
                        continue
                    if next is None or len(p) < len(path[next]):
                        next = c
                if next is None:
                    return False
                current = next
        return final_path

    def find_path(self, arr, from_coords, to_coords: list):
        """Dijkstras pathfinding algo that moves in steps of 3.
        First goes from A to B, then from the middle of the just created path to C and so on....
        :param arr -> The array with mapped elements
        :param from_coords -> A tuple of coordinates to start from
        :param to_coords   -> A list of tuples of coordinates to coordinate to"""

        path_steps = []
        y, x = from_coords
        for end_coord in to_coords:
            s = (
                3 if isinstance(end_coord, tuple) else 1
            )  # Just trying to make poi pathfinding work
            visited = set()
            # First iteration draw a straight path. The ones after that start from the middle of the current known path
            if path_steps:
                current = path_steps[len(path_steps) // 2]
            else:
                current = from_coords
            path = {current: [current]}
            while current:
                for coord in self.checker.coords_around(arr, current, steps=s):
                    y, x = coord
                    dist = len(path[current]) + 1
                    if coord not in path or dist < len(path[coord]):
                        path[coord] = path[current] + [coord]

                visited.add(current)
                if isinstance(end_coord, list):
                    if self.next_to_path(arr, end_coord, current):
                        path_steps.extend(path[current])
                        break
                else:
                    if current == end_coord:
                        path_steps.extend(path[current])
                        break
                    # If under 3 tiles away in on direction from the end, add current path + end coord to the final path
                    # fill_path will fill the skipped coordinates
                    if self.end_close_enough(current, end_coord):
                        path_steps.extend(path[current] + [end_coord])
                        break
                next = None
                for c, p in path.items():
                    y, x = c
                    if arr[y][x] != -1:
                        continue
                    # If 3 step path contains anything other than -1
                    if [a for a in self.fill_path([current, c]) if arr[a] != -1]:
                        continue
                    if c in visited:
                        continue
                    if next is None or len(p) < len(path[next]):
                        next = c
                if next is None:
                    return False
                current = next
        # Fill in the blanks caused by taking 3 steps at a time
        final_path = self.fill_path(path_steps)
        return final_path

    def create_road_path(self, arr, from_coords, to_coords: list):
        """Uses dijkstras pathfinding algo, and creates wiggliness in the shortest path found
        First goes from A to B, then from the middle of the just created path to C and so on....
        :param arr -> The array with mapped elements
        :param from_coords -> A tuple of coordinates to start from
        :param to_coords   -> A list of tuples of coordinates to coordinate to"""
        arr = arr != -1
        arr = self.reduce_axis(self.reduce_axis(arr).T).T
        from_coords = tuple([x // 2 for x in from_coords])
        to_coords = [tuple([x // 2 for x in end_coords]) for end_coords in to_coords]

        timer = time.perf_counter()
        open_cells = list(zip(*np.nonzero(arr == False)))
        random.shuffle(open_cells)
        if not (witness := self.find_road_path(arr, from_coords, to_coords)):
            raise Exception(f"Could not find a road from {from_coords} to {to_coords}")
        while True:
            if not open_cells:
                if self.verbose:
                    print("Finding out the road took", time.perf_counter() - timer)
                return witness
            c = open_cells.pop(0)
            y, x = c
            arr[y][x] = True
            if c in witness:
                # find_path considers everything other than -1 as an obstacle
                if new_path := self.find_road_path(arr, from_coords, to_coords):
                    witness = new_path
                else:
                    arr[y, x] = False

    def create_path(self, arr, from_coords, to_coords: list, max_wiggle=5):
        """Uses dijkstras pathfinding algo, and creates wiggliness in the shortest path found
        First goes from A to B, then from the middle of the just created path to C and so on....
        :param arr -> The array with mapped elements
        :param from_coords -> A tuple of coordinates to start from
        :param to_coords   -> A list of tuples of coordinates to coordinate to"""
        timer = time.perf_counter()
        arr = copy.deepcopy(arr)
        wiggles = 0
        search_duration = 0
        if not (witness := self.find_path(arr, from_coords, to_coords)):
            raise Exception(
                f"Could not find a POI path from {from_coords} to {to_coords}"
            )
        while True:
            if wiggles == max_wiggle or search_duration > 1.0:
                if self.verbose:
                    print("Finding out the POI path took", time.perf_counter() - timer)
                return witness
            c = random.choice(witness)
            y, x = c
            # find_path considers everything other than -1 as an obstacle
            arr[y][x] = 0
            search_start = time.perf_counter()
            if new_path := self.find_path(arr, from_coords, to_coords):
                search_duration = time.perf_counter() - search_start
                wiggles += 1
                witness = new_path
            else:
                return witness

    def largen_path(self, array, path):
        """Walk through path and append all coordinates around it to the path. Widens the path by 2"""
        large_path = set()
        for coord in path:
            large_path = large_path | {
                tuple(x) for x in self.checker.cube_around(array, coord)
            }
        # large_path == 3 wide
        return large_path

    def fill_path(self, path):
        # The pathfinding moves in steps of 3, so fill in the blank coordinates
        filled_path = []
        prev_coord = False
        for coord in path:
            if prev_coord:
                y, x = coord
                prev_y, prev_x = prev_coord
                if abs(y - prev_y) > 3 or abs(x - prev_x) > 3:
                    prev_coord = coord
                    continue
                if y != prev_y:
                    if y > prev_y:
                        for y in range(prev_y + 1, y):
                            filled_path.append((y, x))
                    else:
                        for y in range(prev_y - 1, y, -1):
                            filled_path.append((y, x))
                if x != prev_x:
                    if x > prev_x:
                        for x in range(prev_x + 1, x):
                            filled_path.append((y, x))
                    else:
                        for x in range(prev_x - 1, x, -1):
                            filled_path.append((y, x))
            prev_coord = coord
            filled_path.append(coord)
        return filled_path
