"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, PuzzleItem, TradeItem, Player

# Note: You may add helper functions, classes, etc. here as needed


def reverse_movement(player, last_choice):
    """reverses movement due to certain conditions"""
    if last_choice == "go north":
        player.y += 1  # Move back south
    elif last_choice == "go south":
        player.y -= 1  # Move back north
    elif last_choice == "go east":
        player.x -= 1  # Move back west
    elif last_choice == "go west":
        player.x += 1  # Move back east


def handle_action(world: World, player: Player, chc: str):
    """Handles the players choices"""
    # Extract the current location of the player
    loc = world.get_location(player.x, player.y)
    if chc == "look":
        # Display the full description of the location
        print(loc.f_desc)
        for it in loc.items:
            print(it.name)
    elif chc == "inventory":
        # Display the player's inventory
        print("Inventory:", player.inventory)
    elif chc == "score":
        # Display the player's score
        print(f"Score: {player.points}")
    elif chc == "map":
        # Display the player's score
        map_maker(world, player)
    elif chc == "pick-up item":
        # Player picks up item and item is removed from location
        print("What item do you want to pick up?")
        pick_item = input("item to be picked up: ")
        if pick_item in w.items:
            p_item = world.items[pick_item]
            if isinstance(p_item, PuzzleItem) and p_item.start_position == loc.map_spot and p_item in loc.items:
                handle_puzzle(world, player, p_item)
            else:
                player.inventory.append(pick_item)
                loc.items.remove(p_item)
                print(f"you picked up {pick_item}")
        else:
            print("that item is not in the room or is not an item")
    elif chc == "drop item":
        # Player drops the item and item is now located within new location
        print("What item do you want to drop?")
        drop_item = input("item wished to be dropped: ")
        if drop_item in player.inventory:
            player.inventory.remove(drop_item)
            loc.items.append(world.items[drop_item])
            print(f"you dropped the {drop_item}")
        else:
            print("you do not have that item in your inventory")
    elif chc == "use item":
        # Player selects item to use
        print("What item do you want to use")
        use_item = input("item wished to be use: ")
        if use_item in player.inventory:
            handle_trade(world, player, world.items[use_item])
        else:
            print("you do not have that item, or it does not exist")
    elif chc == "quit":
        # Exit the game loop
        p.victory = True
        print("Quitting the game.")
    elif chc == "back":
        # Exit the game loop
        print(".")
    else:
        print("Non-valid input, returning to menu")


def map_maker(world: World, player: Player):
    """
        Prints out the map with the player's position marked by an 'X'.
    """
    print("X is where you are")
    for row in range(0, len(world.map)):
        print()
        for num in range(0, len(world.map[0])):
            if player.x == num and player.y == row:
                print(" X  ", end="")
            elif len(str(world.map[row][num])) == 2:
                print(str(world.map[row][num]) + "  ", end="")
            else:
                print(" " + str(world.map[row][num]) + "  ", end="")
    print()


def handle_trade(world: World, player: Player, item: Item):
    """
    Handles a trade in the game so a player can exchange an item for another.
    """
    loc = world.get_location(player.x, player.y)
    if not loc.items:
        print("That item has no use or cannot be used here")
    for items in loc.items:
        if isinstance(items, TradeItem) and item.end == loc.map_spot and items.trade_key == item.name:
            print(f"You used the {item.name} successfully! You {items.trade_line}")
            player.inventory.remove(item.name)
            player.inventory.append(items.name)
            player.points += item.target_points
        else:
            print("That item has no use or cannot be used here")
            pass


def handle_puzzle(world: World, player: Player, puzzle: PuzzleItem):
    """
    Handles the interaction of a player attempting to pick up an item that requires
    solving a puzzle.
    """
    loc = world.get_location(player.x, player.y)
    correct = False
    quits = False
    while not(correct or quits or puzzle.solved):
        print(f"To pick up the item you must pass a Puzzle!\nthe question is {puzzle.puzzle_q}")
        answer = input("Answer here: ")
        if answer == puzzle.puzzle_a:
            print(f"Correct!!! you picked up the {puzzle.name}")
            player.points += puzzle.target_points
            correct = True
            puzzle.solved = True
        elif answer == "quit":
            quits = True
        else:
            print("Incorrect ;w;, Try again or enter 'quit' to quit trying and return")
    if puzzle.solved is True:
        player.inventory.append(puzzle.name)
        loc.items.remove(world.items[puzzle.name])


if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(1, 1)  # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "map", "use item", "pick-up item", "drop item", "quit", "back"]
    counter = 0
    choice = ""
    while not p.victory and counter <= 80:
        location = w.get_location(p.x, p.y)
        if location is None:
            print("You can't go that way.")
            reverse_movement(p, choice)
            continue
        if location.map_spot in [4, 7]:
            required_item = "Key" if location.map_spot == 4 else "TCard"
            if required_item not in p.inventory and location.visited is False:
                print(f"You are missing an item to enter this location: {required_item}")
                reverse_movement(p, choice)
                continue
            else:
                if required_item == "Key" and "Key" in p.inventory:
                    p.points += w.items["Key"].target_points
                    p.inventory.remove("Key")
                # Allowed to enter, handle as normal location
                pass

            # Normal location handling (first visit or subsequent visits)
        if not location.visited:
            print(location.f_desc)
            for it in location.items:
                print(it.name)
            location.visited = True
            p.points += location.points
        else:
            print(location.b_desc)

        print("What to do? \n")
        print("[menu]")
        for action in location.avail_action:
            print("go " + action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
            handle_action(w, p, choice)
        elif choice == "go north":
            p.y = p.y - 1
        elif choice == "go south":
            p.y = p.y + 1
        elif choice == "go east":
            p.x = p.x + 1
        elif choice == "go west":
            p.x = p.x - 1
        else:
            print("invalid action, try again (case sensitivity is required)")

        counter += 1

        if (('Cheat Sheet' in p.inventory and 'Lucky Pencil' in p.inventory and 'TCard' in p.inventory) and
                (w.get_location(p.x, p.y).map_spot == 16)):
            print("You did it! You reached the exam on time and did AMAZING!")
            p.victory = True
    if choice == "quit" or counter > 80:
        print("YOU LOSE, DO BETTER NEXT TIME")
