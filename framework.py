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
player = {"health": 10, "damage": 1, "defence": 0, "gold": 0, "weapon": None, 'seasoned': False, "chicken": False}
wave = 0
ENEMYHP_SCALING = 1.2
ENEMYDMG_SCALING = 1.1


def tutorial():
    """
    A function that plays a tutorial for the user. This includes three cycles of the main core
    game phases.
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
        
def battle(enemy_stats: dict, player: dict, wave: int):
    """
    A function that runs a battle process between the user and an enemy.
    """
    
    global gold, dead

    # Establishing temporary variables for the battle
    hp = player["health"]
    dmg = player["damage"]
    defence = player["defence"]
    
    enemy_hp = enemy_stats["hp"]
    enemy_dmg = enemy_stats["dmg"]

    # Prints information about the boss
    print(f"Wave: {wave}")
    print(f"You are about to fight {enemy_stats['name']}!")
    print(f"""{enemy_stats['name']} statistics:
Health: {enemy_hp} 
Damage: {enemy_dmg}""")
    ready = input("Press any key to start: ")
    print("--------------------------------------------------")

    # Loops through a fight until either party falls below 0 hp.
    while hp > 0 and enemy_hp > 0:
        print()
        if player['weapon'] != None:
            damage_c = dmg * player["weapon"]["damage"]
            enemy_hp = round((enemy_hp - damage_c), 2)
        else:
            enemy_hp = round((enemy_hp - dmg), 2)

        hp = round(hp - (enemy_dmg * (1 - (defence/10))), 2)

        # Prevents hp from going below 0
        if enemy_hp < 0:
            enemy_hp = 0
        if hp < 0:
            hp = 0
        
        print(f"""{enemy_stats['name']}'s Health: {enemy_hp} 
Your Health: {hp}
        """)
        
    print("--------------------------------------------------")

    # Checks the result of the battle and rewards the player accordingly
    if hp == 0 and enemy_hp == 0:
        print(f"You and the enemy simultaneously collapsed. You got away but couldn't safely pick up the gold.")
    elif hp > 0:
        gold_dropped = randint(1,1)
        print(f"You won! You gain {gold_dropped} gold!")
        player["gold"] += gold_dropped
    else:
        print("You died :(")
        dead = True

def upgrade():
    """
    A function that allows the user to upgrade their core stats.
    """
    stats = {'health': {'cost': 1, 'increment': 2}, 'defence': {'cost': 1, 'increment': 1, 'max': 5}, 'damage': {'cost': 2, 'increment': 1}}
    
    exit = False

    # Asks the player what they would like to do until they run out of gold or want to exit
    while exit == False:
        print(f"------------ UPGRADE ------------")
        print(f"Gold: {player['gold']}, Health: {player['health']}, Defence: {player['defence']}, Damage: {player['damage']}")
        for stat in stats:
            print(f"{stat} - cost: {stats[stat]['cost']}")
        
        upgrade_choice = input("What would you like to upgrade? [Type 'X' to exit] ")

        # Evalutes the player's choice and upgrades accordingly
        if upgrade_choice in stats.keys():
            if player["gold"] >= stats[upgrade_choice]["cost"]:
                if upgrade_choice == "defence":
                    if player["defence"] >= stats['defence']['max']:
                        print("Defence is maxed!")
                    else:
                        player[upgrade_choice] += stats[upgrade_choice]['increment']
                        player["gold"] -= stats[upgrade_choice]['cost']
                else:
                    player[upgrade_choice] += stats[upgrade_choice]['increment']
                    player["gold"] -= stats[upgrade_choice]['cost']
                
            else:
                print("You do not have enough gold.")
                
        elif upgrade_choice == "X":
            exit = True
        else:
            print("Invalid choice!")
            
    print(f"Gold: {player['gold']}, Health: {player['health']}, Defence: {player['defence']}, Damage: {player['damage']}")

def weapon_shop():
    """
    A function that displays available weapons and allows the user to buy them.
    """
    
    global player

    weapons = [
    {"name": "Chopsticks", "cost": 5, "damage": 1.25},
    {"name": "Spatula", "cost": 8, "damage": 1.5},
    {"name": "Knife", "cost": 10, "damage": 1.75},
    {"name": "Frying Pan", "cost": 12, "damage": 2},
        ]
    
    exit = False


    # Prints the available weapons
    for weapon in weapons:
        print(f"{weapon['name']} ({weapon['damage']} dmg): {weapon['cost']} gold")

    
    while exit == False:
        weapon_choice = int(input("What do you choose to buy? [1/2/3/4/0]: "))

        # Evaluates the player's choice and checks if they have enough gold to afford the item.
        if weapon_choice in [1,2,3,4]:
            if weapons[weapon_choice-1]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif player['gold'] < weapons[weapon_choice-1]["cost"]:
                print("You do not have enough money.")
            else:    
                player["weapon"] = weapons[weapon_choice-1]
                player['gold'] -= weapons[weapon_choice-1]["cost"]
                weapons[weapon_choice-1]["cost"] = "SOLD :("
                print(f"You successfully bought a {weapons[weapon_choice-1]['name']}. You now have {player['gold']} gold.")
            
        elif weapon_choice == 0:
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
    """
    A function that creates random interactive events.
    """
    global player
    
    number = randint(1,4) 
    while number in completed:
        number = randint(1,4)
        
    completed.append(number)

    # Butcher Event
    if number == 1:
        print("You meet a butcherer.")
        print("He offers you a job to tenderize his meats... ")
        choice = input("Do you accept? [y/n] ")
        if choice == 'y':
            print("During the process, you gain strength, increasing your damage. He also pays you 1 gold for your time.")
            player['gold'] += 1
            player['damage'] += 1
        if choice == 'n':
            print("He asks you if you would sell him a cut of your own meat... ")
            choice = input("Will you sell him your left arm? [y/n] ")
            if choice == 'y':
                print("He buys your left arm for 15 gold. In the process, you lose a lot of blood. The loss of your arm also makes it difficult to fight. Your damage and health is halved. ")
                player['gold'] += 15
                player['damage'] /= 2
                player['health'] /= 2
            elif choice == 'n':
                print("You simply leave his store.")

    # Market Event
    if number == 2:
        print("You come across a food market.")
        choice = input("Do you buy milk, fried chicken, rice, a chili pepper, or nothing? [1/2/3/4/5] ")
        while choice not in ["1","2","3","4","5"]:
            choice = input("What is your decision? [1/2/3/4/5] ")
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

    # Spices Event
    if number == 3:
        print("You find a stash of 11 herbs and spices.")
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
        else:
            print("You keep the spices.")
            player['seasoned'] = True
            
    # Sacrifice Event
    if number == 4:
        print("you find a coin on the ground.")
        player['gold'] += 1
        
        
def reset():
    """
    A function that resets the primary game variables.
    """
    
    global dead, weapons, player, wave
    enemy = {"name": "Knight", "hp": 5, "dmg": 1}
    dead = False
    player = {"health": 10, "damage": 1, "defence": 0, "gold": 0, "weapon": None, 'seasoned': False, "chicken": False}
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
    new_enemy['hp'] = round((old_enemy['hp'] * ENEMYHP_SCALING), 2)
    new_enemy['dmg'] = round((old_enemy['dmg'] * ENEMYDMG_SCALING), 1)
    return new_enemy

def main():
    global dead, wave

    # Establishing Variables
    campaign_bosses = [
    {"name": "Ronald McDonald", "hp": 25, "dmg": 1, "ingredient": "potatoes"},
    {"name": "Wendy", "hp": 20, "dmg": 4, "ingredient": "rice"},
    {"name": "Colonel Sanders", "hp": 30, "dmg": 6, "ingredient": "chicken breasts"},
    {"name": "Gordon Ramsay", "hp": 50, "dmg": 8, "ingredient": "onions"}
                  ]
    completed_events = []
    close = False

    # Introduction
    print("Welcome to Medieval Munchies!")
    run_tutorial = input("Do you want a tutorial? [y/n] ")
    if run_tutorial == "y":
        tutorial()

    # Initiating Game
    while close == False:
        reset()
        enemy = {"name": "Knight", "hp": 5, "dmg": 1}
        while dead == False and wave < 20: 
            wave += 1
            enemy = progress(enemy)

            # Boss Battle
            if wave % 5 == 0:
                print("--------------| BOSS BATTLE |--------------")
                print("You meet a chef...")
                battle(campaign_bosses[round(wave/5 - 1)], player, wave)
                if dead == False:

                    # Colonel Sanders + Spices Event
                    if campaign_bosses[round(wave/5 - 1)]['name'] == "Colonel Sanders":
                        if player['seasoned'] == True:
                            print("Looks like you found my secret 11 herbs and spices...")
                            input("Press enter to continue...")
                            print("The Colonel gives you a bucket of Fried Chicken.")
                            player['chicken'] = True
                            input("Press enter to continue...")   
                            print()
                            
                    print(f"The chef tips you 5 gold for your service and drops you his ingredient: {campaign_bosses[round(wave/5 - 1)]['ingredient']}")
                    player['gold'] += 5

            # Event (waves 3, 8, 13, 18)
            elif wave % 10 == 3 or wave % 10 == 8:
                random_event(completed_events)

            # Normal Battle
            else:
                battle(enemy, player, wave)
                
            if wave < 20:
                player['health'] = round(player['health'], 2)
                player['defence'] = round(player['defence'], 2)
                player['damage'] = round(player['damage'], 2)
                preperation()


        # Ending Sequences
        if dead == False:
            if player['chicken'] == True:
                choice = input("Do you feed the chef the Colonel's chicken or your own dish? [1,2]")
            else:
                choice = input("Press any key to present your dish... ")
            
            if choice == "1":
                print("------- Colonel's Chicken Ending -------")
                print("You gave Mr. Banjevic the best chicken he's ever had!")
            else:
                print("------- Normal Ending -------")
                print("GOOD JOB! You collected all of the ingredients and prepared an amazing meal for Mr. Banjevic!")

            

        # Restart Game
        stop = input("Would you like to play again? [y/n] ")
        if stop != "y":
            close = True

    print("See you next time!")        
        

main()
        
