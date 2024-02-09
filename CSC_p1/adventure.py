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
from game_data import World, Item, Location, Player

# Note: You may add helper functions, classes, etc. here as needed


def reverse_movement(player, last_choice):
    """reverses movement due to certain conditions"""
    if last_choice == "go north":
        player.y -= 1  # Move back south
    elif last_choice == "go south":
        player.y += 1  # Move back north
    elif last_choice == "go east":
        player.x -= 1  # Move back west
    elif last_choice == "go west":
        player.x += 1  # Move back east


def handle_action(world, player, choice):
    """Handles the players choices"""
    # Extract the current location of the player
    location = world.get_location(p.x, p.y)

    if choice == "look":
        # Display the full description of the location
        print(location.f_desc)
    elif choice == "inventory":
        # Display the player's inventory
        print("Inventory:", player.inventory)
    elif choice == "score":
        # Display the player's score
        # Assuming 'score' is an attribute of Player class
        print(f"Score: {player.points}")
    elif choice == "back":
        # Exit the game loop
        print(".")
    elif choice == "quit":
        # Exit the game loop
        print("Quitting the game.")
        player.victory = True
    else:
        print("Non-valid input, returning to menu")
    # Add more actions as needed based on your game design
# Note: You may modify the code below as needed; the following starter template are just suggestions


if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(1, 1)  # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "quit", "back"]
    counter = 0
    choice = ""
    while not p.victory and counter <= 80:
        location = w.get_location(p.x, p.y)
        if location.map_spot in [4, 7]:
            required_item = "Key" if location.map_spot == 4 else "Tcard"
            if required_item not in p.inventory:
                print(f"You are missing an item to enter this location: {required_item}")
                reverse_movement(p, choice)
                continue
            else:
                # Allowed to enter, handle as normal location
                pass  # This can be replaced with the normal handling code for entering a location

            # Normal location handling (first visit or subsequent visits)
        if not location.visited:
            print(location.f_desc)
            location.visited = True
            p.points += location.points  # Assuming points need to be added on first visit
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

        if (('Cheat Sheet' and 'Lucky Pencil' and 'Tcard' in p.inventory) and
                (w.get_location(p.x, p.y) == 16)):
            print("You did it! You reached the exam on time and did AMAZING!")
            p.victory = True

        #  TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
