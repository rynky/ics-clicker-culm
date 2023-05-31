from random import randint
"""
import pygame
import pygame.display as display
from random import randint

window = display.set_mode((1280,720))
display.set_caption("ICS3U - Raiyan and Raymond")
display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
"""

# ----- Raymond's edits (getting the base game to function) ----- #

# Establish global variables
dead = False
player = {"health": 10, "damage": 1, "defence": 0, "gold": 0, "weapon": None}
wave = 0


def tutorial():
    """
    A function that plays a tutorial for the user. This includes the core game functions.
    """
    
    tutorial_bosses = [
    {"name": "Trainer", "hp": 5, "dmg": 0},
    {"name": "Raiyan", "hp": 4, "dmg": 2},
    {"name": "Raymond", "hp": 10, "dmg": 1}
         ]

    # Giving the player information
    print("Your goal is to survive and kill the final boss in this game! ")
    print((input("Press enter to continue... "))) 
    print("However, there are many foes between you and the boss! ")
    print((input("Press enter to continue... ")))
    print("Try to beat these weak opponents first! ")
    print((input("Press enter to continue... ")))
    print()

    # Runs through three cycles of battling and preparing
    for boss in tutorial_bosses:
        battle(boss, player, "TUTORIAL")
        preperation()

    skip = input("Great job! Good luck with the rest of the game! ")
        
def battle(boss_stats: dict, player: dict, wave: int):
    """
    A function that runs a battle process between the user and an enemy.
    """
    
    global gold, dead

    # Establishing temporary variables for the battle
    hp = player["health"]
    dmg = player["damage"]
    defence = player["defence"]
    
    boss_hp = boss_stats["hp"]
    boss_dmg = boss_stats["dmg"]

    # Prints information about the boss
    print(f"Wave: {wave}")
    print(f"You are about to fight {boss_stats['name']}!")
    print(f"""{boss_stats['name']} statistics:
Health: {boss_hp} 
Damage: {boss_dmg}""")
    ready = input("Press any key to start: ")
    print("--------------------------------------------------")

    # Loops through a fight until either party falls below 0 hp.
    while hp > 0 and boss_hp > 0:
        print()
        if player['weapon'] != None:
            damage_c = dmg * player["weapon"]["damage"]
            boss_hp = round((boss_hp - damage_c), 2)
        else:
            boss_hp = round((boss_hp - dmg), 2)

        hp = round(hp - (boss_dmg * (1 - (defence/20))), 2)

        # Prevents hp from going below 0
        if boss_hp < 0:
            boss_hp = 0
        if hp < 0:
            hp = 0
        
        print(f"""{boss_stats['name']}'s Health: {boss_hp} 
Your Health: {hp}
        """)
        
    print("--------------------------------------------------")

    # Checks the result of the battle and rewards the player accordingly
    if hp == 0 and boss_hp == 0:
        print(f"You and the enemy simultaneously collapsed. You got away but couldn't safely pick up the gold.")
    elif hp > 0:
        gold_dropped = randint(1,2)
        print(f"You won! You gain {gold_dropped} gold!")
        player["gold"] += gold_dropped
    else:
        print("You died :(")
        dead = True

def upgrade():
    """
    A function that allows the user to upgrade their core stats.
    """
    exit = False

    # Asks the player what they would like to do until they run out of gold or want to exit
    while exit == False:
        print(f"Gold: {player['gold']}, Health: {player['health']}, Defence: {player['defence']}, Damage: {player['damage']}")
        upgrade_choice = input("What would you like to upgrade? [Type 'X' to exit] ")

        # Evalutes the player's choice and upgrades accordingly
        if upgrade_choice == "health":
            player["health"] += 2
            player["gold"] -= 1
        elif upgrade_choice == "defence":
            if player["defence"] >= 15:
                print("Defence is maxed!")
            else:
                player["defence"] += 1
                player["gold"] -= 1
        elif upgrade_choice == "damage":
            player["damage"] += 1
            player["gold"] -= 1
        elif upgrade_choice == "X":
            exit = True
        else:
            print("Invalid choice!")
            
    print(f"Gold: {player['gold']}, Health: {player['health']}, Defence: {player['defence']}, Damage: {player['damage']}")

def weapon_shop():
    """
    A function that displays available weapons and allows the user to buy them.
    """
    
    global player, gold

    weapons = [
    {"name": "Slipper", "cost": 5, "damage": 2},
    {"name": "Belt", "cost": 10, "damage": 3},
    {"name": "Sword", "cost": 20, "damage": 5},
    {"name": "Pencil", "cost": 120, "damage": 10},
        ]
    
    exit = False

    # Prints the available weapons
    for weapon in weapons:
        print(f"{weapon['name']} ({weapon['damage']} dmg): {weapon['cost']} gold")

    
    while exit == False:
        weapon_choice = input("What do you choose to buy? [X to exit]: ")

        # Evaluates the player's choice and checks if they have enough gold to afford the item.
        if weapon_choice == "slipper":
            if weapons[0]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif player['gold'] < weapons[0]["cost"]:
                print("You do not have enough money.")
            else:    
                player["weapon"] = weapons[0]
                player['gold'] -= weapons[0]["cost"]
                weapons[0]["cost"] = "SOLD :("
                print(f"You successfully bought a {weapon_choice}. You now have {player['gold']} gold.")
            
        elif weapon_choice == "belt":
            if weapons[1]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif player['gold'] < weapons[1]["cost"]:
                print("You do not have enough money.")
            else:    
                player["weapon"] = weapons[1]
                player['gold'] -= weapons[1]["cost"]
                weapons[1]["cost"] = "SOLD :(" 
                print(f"You successfully bought a {weapon_choice}. You now have {player['gold']} gold.")
                
        elif weapon_choice == "sword":
            if weapons[2]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif player['gold'] < weapons[2]["cost"]:
                print("You do not have enough money.")
            else:    
                player["weapon"] = weapons[2]
                player['gold'] -= weapons[2]["cost"]
                weapons[2]["cost"] = "SOLD :(" 
                print(f"You successfully bought a {weapon_choice}. You now have {player['gold']} gold.")
                
        elif weapon_choice == "pencil":
            if weapons[3]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif player['gold'] < weapons[3]["cost"]:
                print("You do not have enough money.")
            else:    
                player["weapon"] = weapons[3]
                player['gold'] -= weapons[3]["cost"]
                weapons[3]["cost"] = "SOLD :(" 
                print(f"You successfully bought a {weapon_choice}. You now have {player['gold']} gold.")
            
        elif weapon_choice == "X":
            exit = True
        else:
            print("Invalid choice!")

    
def preperation():
    """
    A function that displays a menu for the user in between battles.
    This includes upgrading and buying items.
    """
    skip = False

    # Checks if the user is dead
    if dead == True:
        print("Good luck next time!")

    # Prints information for the player and asks for their choice
    else:
        print("You set up camp again after surviving another boss encounter. Take time to rest and prepare for the next one.")
        while skip == False:
            print(f"You have {player['gold']} gold.")
            prep_choice = input("Do you want to upgrade, buy a new weapon, or skip? ")
            if prep_choice == "upgrade":
                upgrade()
            elif prep_choice == "buy":
                print()
                weapon_shop()
            elif prep_choice == "skip":
                skip = True
            else:
                print("Invalid choice!")
    print()


def random_event(completed):
    global player
    
    number = randint(1,4) 
    while number in completed:
        number = randint(1,4)
        
    completed.append(number)


    if number == 1:
        print("You meet a butcherer.")
    if number == 2:
        print("You come across a grocery store.")
        choice = input("Do you buy milk, fried chicken, rice, a chili pepper, or nothing? [1/2/3/4/5]")
        
        if choice == "1":
            print("The milk strengthen your bones, giving bonus defence.")
            player["defence"] += 2
        elif choice == "2":
            print("The greasy chicken increases your blood pressure, negatively impacting your health.")
            player["health"] *= 0.9
        elif choice == "3":
            print("The rice fills you up, envigorating you and granting bonus health.")
            player["health"] *= 1.2
        elif choice == "4":
            print("The chili pepper sets your mouth on fire, granting a small bonus to your damage.")
            player['damage'] += 1
        elif choice == "5":
            print("You just walk away.")
    if number == 3:
        print("You find a stash of spices.")
        if player["weapon"] != None:
            choice = input("Do you choose to season your weapon or consume the spices yourself? [1, 2] ")
        else:
            choice = input("Do you consume all of the spices? [2, 3] ")
            
        if choice == "1":
            print("You enhance your weapon with flavour, doubling its damage.")
            player['weapon']['damage'] *= 2
        elif choice == "2":
            print("You consume the spices, sacrificing your health for damage and defence.")
            player['defence'] *= 1.1
            player['health'] *= 0.9
            player['damage'] *= 1.25
        elif choice == "3":
            print("You just walk away.")
            
            
    if number == 4:
        print("You ")
        
        
def reset():
    """
    A function that resets the primary game variables.
    """
    
    global dead, weapons, player, wave
    dead = False
    player = {"health": 10, "damage": 1, "defence": 0, "gold": 0, "weapon": None}
    wave = 0
    weapons = [
        {"name": "Slipper", "cost": 5, "damage": 2},
        {"name": "Belt", "cost": 10, "damage": 3},
        {"name": "Sword", "cost": 20, "damage": 5},
        {"name": "Pencil", "cost": 120, "damage": 10},
              ]

def progress(old_enemy: dict) -> dict:
    """
    A function that increases the difficulty of the game by increasing the stats of the enemy.
    """
    
    new_enemy = {}
    ENEMY_NAMES = ["Archer", "Knight", "Hunter", "a", "b", "c", "d"]

    # Randomly chooses a basic enemy name and multiplies the hp and dmg of the enemy by a constant
    new_enemy['name'] = ENEMY_NAMES[randint(0, len(ENEMY_NAMES)-1)]
    new_enemy['hp'] = round((old_enemy['hp'] * 1.2), 2)
    new_enemy['dmg'] = round((old_enemy['dmg'] * 1.1), 1)
    return new_enemy

def main():
    global dead, wave
    
    campaign_bosses = [
    {"name": "Ronald McDonald", "hp": 25, "dmg": 1},
    {"name": "Colonel Sanders", "hp": 20, "dmg": 4},
    {"name": "Gordon Ramsey", "hp": 20, "dmg": 8},
    {"name": "Mr. Banjevic", "hp": 50, "dmg": 6}
                  ]
    completed_events = []
    
    close = False
    print("Welcome to GAME NAME!")
    run_tutorial = input("Do you want a tutorial? [y/n] ")
    if run_tutorial == "y":
        tutorial()
        
    while close == False:
        enemy = {"name": "Knight", "hp": 5, "dmg": 1}
        reset()
        while dead == False and wave < 20: 
            wave += 1
            enemy = progress(enemy)
            if wave % 5 == 0:
                print("--------------| BOSS BATTLE |--------------")
                print("You meet a chef...")
                battle(campaign_bosses[round(wave/5 - 1)], player, wave)
                if dead == False:
                    print("The boss tips you for your service...")
                    print("You gain 5 extra gold.")
                    player['gold'] += 5
            elif wave % 10 == 3 or wave % 10 == 8:
                random_event(completed_events)
            else:
                battle(enemy, player, wave)
            preperation()

        if dead == False:
            print("GOOD JOB!")
            
        stop = input("Would you like to play again? [y/n] ")
        if stop != "y":
            close = True

    print("See you next time!")        
        

main()
        
