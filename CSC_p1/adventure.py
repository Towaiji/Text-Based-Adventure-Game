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
        print(f"Score: {player.score}")
    elif choice == "back":
        # Exit the game loop
        print(".")
    elif choice == "quit":
        # Exit the game loop
        print("Quitting the game.")
    else:
        print("Non-valid input, returning to menu")
        player.victory = True  # Assuming ending the game sets 'victory' to True
    # Add more actions as needed based on your game design
# Note: You may modify the code below as needed; the following starter template are just suggestions


if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(1, 1)  # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "quit", "back"]

    while not p.victory:
        location = w.get_location(p.x, p.y)
        if location.visited is False:
            print(location.f_desc)
            location.visited = True
        else:
            print(location.b_desc)

        print("What to do? \n")
        print("[menu]")
        for action in location.available_actions():
            print(action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
            handle_action(w, p, choice)


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
