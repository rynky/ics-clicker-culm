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

# Raymond's edits (getting the base game to function)
dead = False
gold = 0
damage = 1
health = 10
defence = 0
equipped_weapon = None
tutorial_bosses = [
    {"name": "Trainer", "hp": 5, "dmg": 0},
    {"name": "Raiyan", "hp": 4, "dmg": 2},
    {"name": "Raymond", "hp": 10, "dmg": 1}
         ]
weapons = [
    {"name": "Slipper", "cost": 5, "damage": 2},
    {"name": "Belt", "cost": 10, "damage": 3},
    {"name": "Sword", "cost": 20, "damage": 5},
    {"name": "Pencil", "cost": 120, "damage": 10},
        ]

# These are for milestones
campaign_bosses = [
    {"name": "RANDOM", "hp": 10, "dmg": 1},
    {},
    {},
    {"name": "Mr. Banjevic", "hp": 10, "dmg": 1}
                  ]
campaign_events = [
    {},
    {},
    {}
]
def tutorial():
    skip = input("Your goal is to survive and kill the final boss in this game! ")
    skip = input("However, there are many foes between you and the boss! ")
    skip = input("Try to beat these weak opponents first! ")
    print()
    for boss in tutorial_bosses:
        battle(boss, damage, health, "TUTORIAL")
        preperation()

    skip = input("Great job! Good luck with the rest of the game! ")
        
def battle(boss_stats, dmg, hp, wave):
    global gold, dead
    
    print(f"Wave: {wave}")
    print(f"You are about to fight {boss_stats['name']}!")
    print(f"""{boss_stats['name']} statistics:
Health: {boss_stats["hp"]} 
Damage: {boss_stats["dmg"]}""")
    ready = input("Press any key to start: ")
    print("--------------------------------------------------")
    
    while hp > 0 and boss_stats['hp'] > 0:
        print()
        if equipped_weapon != None:
            damage_c = dmg * equipped_weapon["damage"]
            boss_stats["hp"] = round((boss_stats["hp"] - dmg_c), 2)
        else:
            boss_stats["hp"] = round((boss_stats["hp"] - dmg), 2)
            
        hp = round(hp - (boss_stats["dmg"] - defence), 2)
        
        if boss_stats["hp"] < 0:
            boss_stats["hp"] = 0
        if hp < 0:
            hp = 0
        
        print(f"""{boss_stats['name']}'s Health: {boss_stats["hp"]} 
Your Health: {hp}
        """)

    if hp == 0 and boss_stats["hp"] == 0:
        print(f"You and the enemy simultaneously collapsed. You got away but couldn't safely pick up the gold.")
        
    elif hp > 0:
        gold_dropped = randint(1,2)
        print(f"You won! You gain {gold_dropped} gold!")
        gold += gold_dropped
    else:
        print("You died :(")
        dead = True

def upgrade():
    global gold, health, defence, damage
    exit = False
    while gold > 0 and exit == False:
        print(f"Gold: {gold}, Health: {health}, Defence: {defence}, Damage: {damage}")
        upgrade_choice = input("What would you like to upgrade? [Type 'X' to exit] ")
        if upgrade_choice == "health":
            health += 2
            gold -= 1
        elif upgrade_choice == "defence":
            defence += 1
            gold -= 1
        elif upgrade_choice == "damage":
            damage += 1
            gold -= 1
        elif upgrade_choice == "X":
            exit = True
        else:
            print("Invalid choice!")
            
    print(f"Gold: {gold}, Health: {health}, Defence: {defence}, Damage: {damage}")


def weapon_shop():
    global equipped_weapon, gold, weapons
    exit = False
    
    for weapon in weapons:
        print(f"{weapon['name']} ({weapon['damage']} dmg): {weapon['cost']} gold")

    
    while exit == False:
        invalid = False
        weapon_choice = input("What do you choose to buy? [X to exit]: ")
        
        if weapon_choice == "slipper":
            if weapons[0]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif gold < weapons[0]["cost"]:
                print("You do not have enough money.")
            else:    
                equipped_weapon = weapons[0]
                gold -= weapons[0]["cost"]
                weapons[0]["cost"] = "SOLD :("
                print(f"You successfully bought a {weapon_choice}. You now have {gold} gold.")
            
        elif weapon_choice == "belt":
            if weapons[1]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif gold < weapons[1]["cost"]:
                print("You do not have enough money.")
            else:    
                equipped_weapon = weapons[1]
                gold -= weapons[1]["cost"]
                weapons[1]["cost"] = "SOLD :(" 
                print(f"You successfully bought a {weapon_choice}. You now have {gold} gold.")
                
        elif weapon_choice == "sword":
            if weapons[2]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif gold < weapons[2]["cost"]:
                print("You do not have enough money.")
            else:    
                equipped_weapon = weapons[2]
                gold -= weapons[2]["cost"]
                weapons[2]["cost"] = "SOLD :(" 
                print(f"You successfully bought a {weapon_choice}. You now have {gold} gold.")
                
        elif weapon_choice == "pencil":
            if weapons[3]["cost"] == "SOLD :(":
                print("You already bought this weapon.")
            elif gold < weapons[3]["cost"]:
                print("You do not have enough money.")
            else:    
                equipped_weapon = weapons[3]
                gold -= weapons[3]["cost"]
                weapons[3]["cost"] = "SOLD :(" 
                print(f"You successfully bought a {weapon_choice}. You now have {gold} gold.")
            
        elif weapon_choice == "X":
            exit = True
        else:
            print("Invalid choice!")
            invalid = True

    
def preperation():
    skip = False
    if dead == True:
        print("Good luck next time!")
        reset()
    else:
        print("You set up camp again after surviving another boss encounter. Take time to rest and prepare for the next one.")
        while skip == False:
            print(f"You have {gold} gold.")
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
        
        
def reset():
    global dead, gold, damage, health, defence, weapons, base_enemy, equipped_weapon, campaign_bosses, campaign_events
    dead = False
    gold = 0
    damage = 1
    health = 10
    defence = 0
    weapons = [
        {"name": "Slipper", "cost": 5, "damage": 2},
        {"name": "Belt", "cost": 10, "damage": 3},
        {"name": "Sword", "cost": 20, "damage": 5},
        {"name": "Pencil", "cost": 120, "damage": 10},
              ]
    equipped_weapon = None
    enemy_base = {"name": "knight", "hp": 5, "dmg": 1}
    campaign_bosses = [
    {"name": "RANDOM", "hp": 10, "dmg": 1},
    {},
    {},
    {"name": "Mr. Banjevic", "hp": 10, "dmg": 1}
                  ]
    campaign_events = [
    {},
    {},
    {}
]

def progress(old_enemy: dict):
    new_enemy = {}
    ENEMY_NAMES = ["Archer", "Knight", "Hunter", "a", "b", "c", "d"]
    new_enemy['name'] = ENEMY_NAMES[randint(0, len(ENEMY_NAMES)-1)]
    new_enemy['hp'] = round((old_enemy['hp'] * 1.2), 2)
    new_enemy['dmg'] = round((old_enemy['dmg'] * 1.1), 1)
    return new_enemy

def main():
    close = False
    print("Welcome to GAME NAME!")
    run_tutorial = input("Do you want a tutorial? [y/n] ")
    if run_tutorial == "y":
        tutorial()
        
    enemy_base = {"name": "Knight", "hp": 5, "dmg": 1}
    global enemy
    while close == False:
        reset()
        for wave in range(1,26): 
            if dead == True:
                break
            print(enemy_base)
            enemy_base = progress(enemy_base)
            enemy = enemy_base
            
            battle(enemy, damage, health, wave)
            print(enemy)
            print(enemy_base)
            preperation()
        stop = input("Would you like to play again? [y/n] ")
        if stop != "y":
            close = True
            
        

main()
        
