"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO, Any


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of the item
        - start: start position of the item on the map
        - target_points: amount of points given when item is used successfully

    Representation Invariants:
        - name != ''
        - start >= 0
        - target_points > 0
    """
    name: str
    start: int
    end: int
    target_points: int

    def __init__(self, name: str, start: int, end: int, target_points: int) -> None:
        """Initialize a new item.
        """
        self.name = name
        self.start_position = start
        self.end = end
        self.target_points = target_points


class PuzzleItem(Item):
    """
        A class that is inherited from the Item class,
        represents the puzzle items in which you have to solve a puzzle to acquire them.

    Instance Attributes:
        - puzzle_q: The question or riddle that makes up the puzzle.
        - puzzle_a: The answer to the puzzle question.
        - solved: A boolean indicating whether the puzzle has been solved.

    Representation Invariants:
        - self.puzzle_q != ''
        - self.puzzle_a is not None
        - isinstance(self.solved, bool)
    """
    puzzle_q: str
    puzzle_a: Any
    solved: bool

    def __init__(self, name: str, start: int, end: int, target_points: int, puzzle_q: str, puzzle_a: Any) -> None:
        """Initialize a new item.
        """
        super().__init__(name, start, end, target_points)
        self.puzzle_q = puzzle_q
        self.puzzle_a = puzzle_a
        self.solved = False


class TradeItem(Item):
    """
        A class that is inherited from the Item class,
        represents the trade items in which you have to trade a key item to acquire them.

    Instance Attributes:
        - trade_line: A message or hint related to the trade.
        - trade_key: The name of the item required for the trade.

    Representation Invariants:
        - self.trade_line != ''
        - self.trade_key != ''
        - self.trade_key exists in world.items
    """
    trade_line: str
    trade_key: str

    def __init__(self, name: str, start: int, end: int, target_points: int, trade_line: str, trade_key: str) -> None:
        """Initialize a new item.
        """
        super().__init__(name, start, end, target_points)
        self.trade_line = trade_line
        self.trade_key = trade_key


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - x: the x position on the map
        - y: the y position on the map
        - b_desc: brief description of the location, given after each subsequent visit
        - f_desc: full description of the location, given at the first time entering the location

    Representation Invariants:
        - x >= 0
        - y >= 0
        - b_desc != ''
        - f_desc != ''
    """
    map_spot: int
    points: int
    avail_action: list[str]
    b_desc: str
    f_desc: str
    items: list[Item]
    visited: bool

    def __init__(self, map_spot, points: int, avail_action: list, b_desc: str, f_desc: str) -> None:
        """Initialize a new location.
        """

        self.map_spot = map_spot
        self.points = points
        self.avail_action = avail_action
        self.b_desc = b_desc
        self.f_desc = f_desc
        self.items = []
        self.visited = False


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - map_spot: position of the player on the map
        - inventory: the inventory of the
        - victory: shows whether the player has won the game or not

    Representation Invariants:
        - map_spot >= 0

    """
    x: int
    y: int
    points: int
    inventory: list
    victory: bool

    def __init__(self,  x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        self.x = x
        self.y = y
        self.points = 0
        self.inventory = []
        self.victory = False


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations: a dictionary mapping location numbers to Location objects
        - items: a dictionary mapping item names to Item objects

    Representation Invariants:
        - map != []
        - location != {}
    """
    map: list[list[int]]
    location: dict[int, Location]
    items: dict[str, Item]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.locations = self.load_locations(location_data)
        self.items = self.load_items(items_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        map_list = []
        for line in map_data:
            row = [int(num) for num in line.strip().split()]
            map_list.append(row)
        return map_list

    def load_locations(self, location_data: TextIO) -> dict[int, Location]:
        """Load the game locations from a file."""
        locations = {}
        content = location_data.readlines()
        i = 0
        while i < len(content):
            line = content[i].strip()
            if line.startswith("LOCATION"):
                loc_id = int(line.split()[1])
                points = int(content[i + 1].strip())
                pos_dir = content[i + 2].strip().split()
                b_desc = content[i + 3].strip()
                f_desc_lines = []
                j = i + 4
                while not content[j].strip().startswith("END"):
                    f_desc_lines.append(content[j].strip())
                    j += 1
                f_desc = "\n".join(f_desc_lines)
                locations[loc_id] = Location(loc_id, points, pos_dir, b_desc, f_desc)
                i = j  # Move to the next location number
            i += 1
        return locations

    def load_items(self, items_data: TextIO) -> dict[str, Item]:
        """Load the game items from a file."""
        items = {}
        for line in items_data:
            parts = line.strip().split()
            item_loc_id = int(parts[0])
            end = int(parts[1])
            target_points = int(parts[2])
            tr_or_pu = parts[3]
            if tr_or_pu == "T":
                trd_line = parts[4]
                trd_key = parts[5]
                name = " ".join(parts[6:])
                item = TradeItem(name, item_loc_id, end, target_points, trd_line, trd_key)
            else:
                pq = parts[4]
                pa = parts[5]
                name = " ".join(parts[6:])
                item = PuzzleItem(name, item_loc_id, end, target_points, pq, pa)
            items[name] = item
            # Assign the item to its starting location
            if item_loc_id in self.locations:
                self.locations[item_loc_id].items.append(item)
        return items

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        if 0 <= y < len(self.map) and 0 <= x < len(self.map[y]):
            location_number = self.map[y][x]
            if location_number == -1:
                return None
            return self.locations.get(location_number)
        return None
