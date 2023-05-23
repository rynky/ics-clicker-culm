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
wave = 0
gold = 0
damage = 1
health = 10
defence = 0
tutorial_bosses = [
    {"name": "Trainer", "hp": 5, "dmg": 0},
    {"name": "Raiyan", "hp": 10, "dmg": 1},
    {"name": "Raymond", "hp": 12, "dmg": 1}
         ]

def tutorial():
    print("Welcome to GAME NAME!")
    skip = input("Your goal is to survive and kill the final boss in this game! ")
    skip = input("However, there are many foes between you and the boss! ")
    skip = input("Try to beat these weak opponents first! ")
    print()
    for boss in tutorial_bosses:
        battle(boss, damage, health)
        preperation()

    skip = print("Great job! Good luck with the rest of the game! ")
        
def battle(boss_stats, dmg, hp):
    global gold, dead, wave
    wave += 1
    
    print(f"Wave: {wave}")
    print(f"You are about to fight {boss_stats['name']}!")
    print(f"""{boss_stats['name']} statistics:
Health: {boss_stats["hp"]} 
Damage: {boss_stats["dmg"]}""")
    ready = input("Press any key to start: ")
    print("--------------------------------------------------")
    while health > 0 and boss_stats['hp'] > 0:
        print()
        boss_stats["hp"] -= dmg
        hp -= (boss_stats["dmg"] - defence)
        
        if boss_stats["hp"] < 0:
            boss_stats["hp"] = 0
        if hp < 0:
            hp = 0
        
        print(f"""{boss_stats['name']}: {boss_stats["hp"]} 
Your Health: {hp}
        """)
        
    if health > 0:
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
        upgrade_choice = input("What would you like to upgrade? [Type 'X' to exit]")
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
    weapons = [
        {"name": "sword", cost: 5, damage: 2},
        {},
        {},
              ]

def preperation():
    skip = False
    if dead == True:
        print("Good luck next time!")
        reset()
    else:
        while True and skip == False:
            print("You successfully defeated the boss. Take time to rest and prepare for the next one.")
            print("You have {gold} gold.")
            prep_choice = input("Do you want to upgrade, buy a new weapon, or skip? ")
            if prep_choice == "upgrade":
                upgrade()
            elif prep_choice == "buy":
                weapon_shop()
            elif prep_choice == "skip":
                skip = True
            else:
                print("Invalid choice!")
        
        
def reset():
    global dead, gold, damage, health, defence
    dead = False
    wave = 0
    gold = 0
    damage = 1
    health = 10
    defence = 0

def main():
    tutorial()
    

main()
        
