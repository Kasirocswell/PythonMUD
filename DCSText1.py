# Dope City Legacy 
# Written by Kasi
from email.header import Header
from pickletools import UP_TO_NEWLINE
import time
import cmd
import textwrap
import sys
import os
import random
import difflib
screen_width = 100

### Intro Screen ###

intro = """
________                         _________ .__  __           .____                                     
\______ \   ____ ______   ____   \_   ___ \|__|/  |_ ___.__. |    |    ____   _________    ____ ___.__.
 |    |  \ /  _ \\____ \_/ __ \  /    \  \/|  \   __<   |  | |    |  _/ __ \ / ___\__  \ _/ ___<   |  |
 |    `   (  <_> )  |_> >  ___/  \     \___|  ||  |  \___  | |    |__\  ___// /_/  > __ \\  \___\___  |
/_______  /\____/|   __/ \___  >  \______  /__||__|  / ____| |_______ \___  >___  (____  /\___  > ____|
        \/       |__|        \/          \/          \/              \/   \/_____/     \/     \/\/     
                       | |
                       |'|            ._____
               ___    |  |            |.   |' .---"|
       _    .-'   '-. |  |     .--'|  ||   | _|    |
    .-'|  _.|  |    ||   '-__  |   |  |    ||      |
    |' | |.    |    ||       | |   |  |    ||      |
 ___|  '-'     '    ""       '-'   '-.'    '`      |____
jgs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


### Player Setup ###

class Player:
    def __init__(self):
        self.name = ""
        self.level = 1
        self.next_level = 10
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.defense = 0
        self.xp = 0
        self.money = 100
        self.location = "i1"
        self.dual_wield = False
        self.status_effects = []
        self.gameover = False
myPlayer = Player()

### Enemy Setup ###

class Enemy:
    def __init__(self, name, health, max_health, location):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.level = 1
        self.attack = 2
        self.defense = 0
        self.cashdrop = 0
        self.cashgain = 0
        self.xpdrop = 100
        self.loot = []
        self.location = location
        self.dual_wield = False
        self.status_effects = []

### Enemeies ###

pickpocket = Enemy("Pickpocket", 20, 20, "a5")
pickpocket2 = Enemy("Pickpocket", 20, 20, "a9")
thug = Enemy("Thug", 20, 20, "a2")
enemies = [pickpocket, thug, pickpocket2]

### Combat System ###

def player_strike():
    player_dmg = myPlayer.attack
    for enemy in enemies:
        if enemy.health > 0 and enemy.location == myPlayer.location:
            print("You attack " + enemy.name + " for " + str(player_dmg) + " damage")
            enemy.health = enemy.health - player_dmg
        else:
            pass

def enemy_strike():
    for enemy in enemies:
        enemy_dmg = enemy.attack
        if myPlayer.health > 0 and enemy.location == myPlayer.location:
            print("You were attacked by " + enemy.name + " for " + str(enemy_dmg) + " damage")
            myPlayer.health = myPlayer.health - enemy_dmg
        else:
            pass

def battle():
    for enemy in enemies:
        fighting = True
        while fighting == True:
            if enemy.health > 0 and myPlayer.health > 0 and enemy.location == myPlayer.location:
                player_strike()
                time.sleep(2)
                if enemy.health > 0:
                    enemy_strike()
                    time.sleep(2)
                else:
                    pass
            elif enemy.health <= 0 and enemy.location == myPlayer.location:
                print("You killed " + enemy.name)
                fighting = False
                time.sleep(5)
                battle_outcome()
                prompt()
            elif myPlayer.health <= 0 and enemy.location == myPlayer.location:
                print("You were killed by " + enemy.name)
                fighting = False
                time.sleep(2)
                prompt()
            else:
                pass
                fighting = False

def battle_outcome():
    for enemy in enemies:
        if enemy.health <= 0 and enemy.location == myPlayer.location:
            myPlayer.xp = myPlayer.xp + enemy.xpdrop
            myPlayer.money = myPlayer.money + enemy.cashdrop
            print("\n")
            print("You gained " + str(enemy.cashdrop) + " Cash")
            print("You gained " + str(enemy.xpdrop) + " XP")
            level_up()
            prompt()
        else:
            pass

def level_up():
    if myPlayer.xp >= myPlayer.next_level:
        myPlayer.level = myPlayer.level + 1
        myPlayer.next_level = myPlayer.level * 1000
        print("\n")
        print("###############")
        print("You leveled up!")
        print("You are now level " + str(myPlayer.level))
        print("You need " + str(myPlayer.next_level) + " for your next level")
        print("###############")
        prompt()

def death():
    return

### Title Selection Logic ###

def help_menu():
    print("Please enter:\n" + "Play - starts the game\n" + "Help - will get you back here\n" + "Quit - will exit the game")
    title_screen_selections()


def title_screen_selections():
    title_screen_on = True
    option = input("> ")
    while title_screen_on == True:
        if option.lower() == "new":
            start_game()
            title_screen_on = False
        elif option.lower() == "help":
                help_menu()
                title_screen_selections()
        elif option.lower() == "quit":
            sys.exit()
        else:
            print("Please enter a valid command")
            option = input("> ")

def title_screen():
    print("################")   
    print("##### Play #####")
    print("##### Help #####")
    print("##### Quit #####")
    print("################")
    title_screen_selections()



### Game Interactivity ###

def print_location():
    print("\n")
    print(("#" * (4 + len(myPlayer.location))))
    print("# " + zonemap[myPlayer.location][ZONENAME] + " #")
    print(zonemap[myPlayer.location][DESCRIPTION])
    print("Enemies: ")
    for enemy in enemies:
        if enemy.health > 0 and enemy.location == myPlayer.location:
            print(enemy.name)
        else:
            pass
    print("#" * (4 + len(myPlayer.location)))

def status_check():
    print("\nName: " +  (myPlayer.name) + 
          "\nLevel: " + str(myPlayer.level) + 
          "\nNext Level: " + str(myPlayer.next_level) +
          "\nHealth: " + str(myPlayer.health) + "/" + str(myPlayer.max_health) + 
          "\nXP: " + str(myPlayer.xp) +  "\nMoney: " + str(myPlayer.money) +  
          "\nAttack: " + str(myPlayer.attack) +  
          "\nDefense: " + str(myPlayer.defense))

def sleep():
    if myPlayer.location == "a5":
        print("Do you want to sleep?")
        action = input("> ")
        if action.lower() in ("yes", "y"):
            myPlayer.health = myPlayer.max_health
            print("You slept in your bed.")
            for enemy in enemies:
                enemy.health = enemy.max_health
                time.sleep(5)
                print_location()
                prompt()
        else:
            prompt()
    else:
        print("You shouldn't sleep on the street here.")
        prompt()

def print_inventory():
    if len(inventory) <= 0:
        print("\n")
        print("Your pockets are empty")
        print_equipment()
    else:
        for item in inventory:
            print("\n")
            print(item.name)

def player_examine():
    print(zonemap[myPlayer.location][EXAMINATION])

def inspect_item():
    print("What item would you like to inspect?\n")
    action = input("> ")
    for item in inventory:
        if len(action) == len(item.name):
            print("\nName: " + item.name + "\nDamage: " + str(item.damage) + "\nArmor: " + str(item.armor) + "\nDescription: " + item.description)
        
def wrongway():
    print("\nYou can't go that way")

def shop():
    return

def game_help():
    print("\nCommand List:\n" + 
             "Say: Print your thoughts to the room\n" + 
             "Move: Allows you to move North, South, East, West, Enter, or Exit\n" + 
             "Look: Examines the current room\n" + 
             "Kill: Attacks any enemies in the room\n" + 
             "Inventory: Displays your current inventory\n" +
             "Status: Displays your current health and level status\n" +
             "Sleep: Sends you to sleep, saves your game, and refills your health\n" + 
             "Inspect: Look closer at an item\n" +
             "Equip/Unequip: Equip or Unequip an item\n" +
             "Shop: Engage in trade with a vendor\n") 

def equip():
    print("Which item would you like to equip?")
    action = input("> ")
    for item in inventory:
        if len(action) == len(item.name) and item.can_equip == True and item.name not in equipped:
            item.equipped = True
            inventory.remove(item)
            equipped.append(item)
            myPlayer.attack = myPlayer.attack + item.damage
            myPlayer.defense = myPlayer.defense + item.armor
            equipment[item.equipped] = True
            print("\n")
            print("You equipped the " + item.name)
        elif len(action) == len(item.name) and item.can_equip == True and item.name in equipped:
            print("\n")
            print("You already have an item equipped in that slot")
        else:
            print("You can't equip that")
            prompt()

def unequip():
    print("Which item would you like to unequip?")
    action = input("> ")
    for item in equipped:
        if len(action) == len(item.name) and item.equipped == True:
            item.equipped = False
            myPlayer.attack = myPlayer.attack - item.damage
            myPlayer.defense = myPlayer.defense - item.armor
            inventory.append(item)
            equipped.remove(item)
            print("\n")
            print("You unequipped the" + item.name)
        else:
            print("You don't have that item equipped")
            prompt()

def print_equipment():
    for item in equipped:
        print(item.slot + ": " + item.name)

def movement_handler(destination):
    myPlayer.location = destination 
    print("\n")   
    print("You have moved to " + zonemap[myPlayer.location][ZONENAME] + ".")
    print_location()

def prompt():
    action = input(">")
    if action.lower() in ("move n", "move north", "move up"):
        destination = zonemap[myPlayer.location][UP]
        if destination == "none":
            wrongway()
            prompt()
        else:
            movement_handler(destination)
            prompt()
    elif action.lower() in ("move s", "move south", "move down"):
        destination = zonemap[myPlayer.location][DOWN]
        if destination == "none":
            wrongway()
            prompt()
        else:
            movement_handler(destination)
            prompt()
    elif action.lower() in ("move w", "move west", "move left"):
        destination = zonemap[myPlayer.location][LEFT]
        if destination == "none":
            wrongway()
            prompt()
        else:
            movement_handler(destination)
            prompt()
    elif action.lower() in ("move e", "move east", "move right"):
        destination = zonemap[myPlayer.location][RIGHT]
        if destination == "none":
            wrongway()
            prompt()
        else:
            movement_handler(destination)
            prompt()
    elif action.lower() in ("enter"):
        destination = zonemap[myPlayer.location][ENTER]
        if destination == "none":
            wrongway()
            prompt()
        else:
            movement_handler(destination)
            prompt()
    elif action.lower() in ("exit"):
        destination = zonemap[myPlayer.location][EXIT]
        if destination == "none":
            wrongway()
            prompt()
        else:
            movement_handler(destination)
            prompt()
    elif action.lower() in "move":
        print("Move where?")
        prompt()
    elif action.lower() == "look":
        print_location()
        print("\n")
        player_examine()
        prompt()
    elif action.lower() in "kill":
        battle()
    elif action.lower() in ("inventory", "inv"):
        print_inventory()
    elif action.lower() in "status":
        status_check()
    elif action.lower() in "sleep":
        sleep()
    elif action.lower() in "equip":
        equip()
    elif action.lower() in "unequip":
        unequip()
    elif action.lower() in "inspect":
        inspect_item()
    elif action.lower() in "shop":
        shop()
    elif "say" in action.lower():
        print(action)
        sentence = action.split(" ")
        sentence.pop(0)
        print(myPlayer.name + ": " + (" ".join(sentence)))
    elif action.lower() in "help":
        game_help()
    else:
        print("Please enter a valid command")
        prompt()

sentence = []

### Item deifinition ###

class Item:
    def __init__(self, name, damage, armor, price):
        self.name = name
        self.damage = damage
        self.armor = armor
        self.price = price
        self.weight = 0
        self.type = "Weapon"
        self.slot = "Right Hand"
        self.description = ""
        self.equipped = False
        self.can_equip = True
        self.usable = False
        self.effect = 0

### Weapons ###

swiss_army_knife = Item("Swiss Army Knife", 10, 0, 10)

### Armor ###

### Items ###

### Inventory Variables ###

inventory = [swiss_army_knife]
equipped = []

### Equipment System ###

HEAD = ""
RIGHT_HAND = ""
LEFT_HAND = ""
UPPER_BODY = ""
LOWER_BODY = ""
FEET = ""

equipment = {HEAD: "none", 
             RIGHT_HAND: "none",
             LEFT_HAND: "none",
             UPPER_BODY: "none",
             LOWER_BODY: "none",
             FEET: "none"}

### Map ###

ZONENAME = ""
DESCRIPTION = "description"
EXAMINATION = "examine"
UP = "up", "north", "n"
DOWN = "down", "south", "s"
LEFT = "left", "west", "w"
RIGHT = "right", "east", "e"
ENTER = "enter"
EXIT = "exit"

solved_places = {"a1": False, "a2": False, "a3": False, "a4": False,
                "a5": False, "a6": False, "a7": False, "a8": False,
                "a9": False 
                }

zonemap = {
    "a1": {
        ZONENAME: "1st & State Street", 
        DESCRIPTION: "The block feels cold.  There isn't much to see here but run down projects", 
        EXAMINATION: "The projects are dark, something doesn't feel right.", 
        UP: "none", 
        DOWN: "a4", 
        LEFT: "none", 
        RIGHT: "a2",
        ENTER: "none",
        EXIT: "none"
        },
    "a2": {
        ZONENAME: "1st & Broadway Avenue", 
        DESCRIPTION: "The large avenue is bustling with business both legel and illicit", 
        EXAMINATION: "Everything is moving to fast to focus on one event here", 
        UP: "none", 
        DOWN: "a5", 
        LEFT: "a1", 
        RIGHT: "a3",
        ENTER: "none",
        EXIT: "none"
        },
    "a3": {
        ZONENAME: "1st & Main Street", 
        DESCRIPTION: "The street is slightly cleaner here, but the city still smells like piss.", 
        EXAMINATION: "You can't get the smell of urine out of your nostrils.", 
        UP: "none", 
        DOWN: "a6", 
        LEFT: "a2", 
        RIGHT: "none",
        ENTER: "none",
        EXIT: "none"
        },
    "a4": {
        ZONENAME: "2nd & State Street", 
        DESCRIPTION: "You hear the sound of children playing on a school yard near by.", 
        EXAMINATION: "Someone is selling drugs outside the school.", 
        UP: "a1", 
        DOWN: "a7", 
        LEFT: "none", 
        RIGHT: "a5",
        ENTER: "none",
        EXIT: "none"
        },
    "a5": {
        ZONENAME: "2nd & Broadway Avenue - Hospital", 
        DESCRIPTION: "You stand outside an old hospital, rusty and falling apart, you can feel death in the air.", 
        EXAMINATION: "The hospital is falling apart.", 
        UP: "a2", 
        DOWN: "a8", 
        LEFT: "a4", 
        RIGHT: "a6",
        ENTER: "i1",
        EXIT: "none"
        },
    "a6": {
        ZONENAME: "2nd & Main", 
        DESCRIPTION: "You see people in their offices doing business", 
        EXAMINATION: "You wonder what kind of money is being made here.", 
        UP: "a3", 
        DOWN: "a9", 
        LEFT: "a5", 
        RIGHT: "none",
        ENTER: "none",
        EXIT: "none"
        },
    "a7": {
        ZONENAME: "3rd & State Street", 
        DESCRIPTION: "The local drug store has the windows boarded.", 
        EXAMINATION: "The drug store is closed", 
        UP: "a4", 
        DOWN: "none", 
        LEFT: "none", 
        RIGHT: "a8",
        ENTER: "none",
        EXIT: "none"
        },
    "a8": {
        ZONENAME: "3rd & Broadway Avenue", 
        DESCRIPTION: "A homeless encampment sits under the freeway overpass.", 
        EXAMINATION: "You can see people vaccinating themselves under the overpass.", 
        UP: "a5", 
        DOWN: "none", 
        LEFT: "a7", 
        RIGHT: "a9",
        ENTER: "none",
        EXIT: "none"
        },
    "a9": {
        ZONENAME: "3rd & Main Street", 
        DESCRIPTION: "There is a large building with the words 'Gun Store' on it.", 
        EXAMINATION: "The line for the gun store extends around the corner", 
        UP: "a6", 
        DOWN: "none", 
        LEFT: "a8", 
        RIGHT: "none",
        ENTER: "i1",
        EXIT: "none"
        },
    "i1": {
        ZONENAME: "Hosptial Lobby", 
        DESCRIPTION: "You stand inside a run down hispital.  There are parients sitting deathly still in their seats, waiting to be seen by the next available doctor", 
        EXAMINATION: "You see a door you could probably exit", 
        UP: "none", 
        DOWN: "none", 
        LEFT: "none", 
        RIGHT: "none",
        ENTER: "none",
        EXIT: "a5"
            },
        }

### Game Loop ###

def start_game():
    print_location()
    main_game_loop()

def main_game_loop():
    while myPlayer.gameover is False:
        prompt()

### GAME START ###
print(intro)
title_screen()