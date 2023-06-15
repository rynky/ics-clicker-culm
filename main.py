# Medieval Munchies by Raiyan and Raymond
# PyGame Imports and Initialization
import pygame
import pygame.display as display
from math import ceil
from random import randint
clock = pygame.time.Clock()
pygame.init()

"""
For this project, each menu will have its respective dictionaries.

Each text entry will be stored as such:
TEXT_NAME : [TEXT_OBJECT, TEXT_COORDINATES]

Similarly, all images will be stored in various image dictionaries, for each screen.
IMAGE_NAME : [IMAGE_OBJECT, IMAGE_COORDINATES]
"""
TITLE_MENU_TEXT = {}
TITLE_MENU_IMAGES = {}

TUTORIAL_MENU_TEXT = {}
TUTORIAL_MENU_IMAGES = {}

MAIN_MENU_TEXT = {}
MAIN_MENU_IMAGES = {}

SHOP_MENU_TEXT = {}
SHOP_MENU_IMAGES = {}

FIGHT_MENU_TEXT = {}
FIGHT_MENU_IMAGES = {}

# Works as Random Access storage for battle stages
# This dictionary will contain the enemies in each stage
# It may be altered at the convenience of the specific stage 
TEMP_ENEMIES = {}

EVENT_MENU_TEXT = {}
EVENT_MENU_IMAGES = {}

UPGRADE_MENU_TEXT = {}
UPGRADE_MENU_IMAGES = {}

VICTORY_MENU_TEXT = {}
VICTORY_MENU_IMAGES = {}

GAME_ENDING_TEXT = {}
GAME_ENDING_IMAGES = {}


#------------Window settings------------# 

WIN = display.set_mode((1080, 720))  # Window Size
HEIGHT = WIN.get_height()
WIDTH = WIN.get_width()
display.set_caption("Medieval Munchies")
display.flip()  # Screen Update
SCREEN_STATUS = "MAIN"  # Track which screen the user is on


#-----------IMPORTANT GLOBALS-----------# 

""" 
RGB Values:
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
"""
ENEMYHP_SCALING = 1.4
ENEMYDMG_SCALING = 1.1

in_battle = False
in_boss_battle = False
dead = False
enemy_cooldown = 0
last_frame = clock.tick(1)
last_enemy = ""
BOSS_MOVEMENT_FACTOR = 0.95

in_event = False
completed_events = []

player = {
    "health": 10, 
    "damage": 1, 
    "defence": 0, 
    "gold": 100, 
    
    # The spoon has a damage of 1
    "weapon": "Spoon",

    # weapon multiplier = 1 + (weapon_damage - 1)/4
    "weapon_multiplier": 1,
    
    "weapon_image": "Images/spoon.png",
    'seasoned': False, 
    "chicken": False,
    "sprite": "Images/chef-character.png",

    'egg': "Images/mystery.png",
    'butter': "Images/mystery.png",
    'flour': "Images/mystery.png",
    'sugar': "Images/mystery.png"
}
STATS_INFO = {'health': {'cost': 1, 'increment': 2}, 'defence': {'cost': 1, 'increment': 1, 'max': 5}, 'damage': {'cost': 2, 'increment': 1}}
wave = 0



#---------------Functions---------------# 

def create_text(name: str,
                screen: dict,
                text: str, 
                font_name: str, 
                font_size: int, 
                color: (int, int, int), 
                text_coordinates: (int, int), 
                anti_aliasing = True):
    """
    Given all the parameters required to initialize text, render a <pygame.font> object.
    Additionally, forward the object and its coordinates to the dictionary <screen>, 
    which stores all the text on the specified game window.
    
    The <anti-aliasing> parameter determines the smoothness of the font, so it is defaulted to True
    for maximum smoothing.
    """

    text_object = pygame.font.SysFont(font_name, font_size).render(text, anti_aliasing, color)

    # Ensures that the coordinates are interpreted based on the center of the image
    screen[name] = [text_object, (text_coordinates[0] - text_object.get_width()/2, text_coordinates[1] - text_object.get_height()/2)]
    

def create_image(name: str, 
                 screen: dict, 
                 image_path: str, 
                 image_coordinates: (int, int), 
                 transparent: bool = False, 
                 scaling = None):
    """
    Given the name of the image <name>, PATH of the image <image_path> and coordinates <image_coordinates>,
    create an image object, and append its name, the object itself, and the coordinates to the dictionary <screen>.

    Additionally, the <transparent> parameter allows the image to be drawn with a transparent background. The <scaling> parameter
    takes a list argument, [x_factor, y_factor], to scale the image. x_factor scales the width, and y_factor scales the height.
    """
    
    # Load the image
    image_object = pygame.image.load(image_path)

    # Convert to transparent, if applicable
    if transparent == True:
        image_object = image_object.convert_alpha()
    else:
        image_object = image_object.convert()
    
    # Scale the image, if applicable
    if not scaling == None:
        image_object = pygame.transform.scale(image_object, (scaling[0], scaling[1]))

    # Add the image to the dictionary
    # Ensures that the coordinates are interpreted based on the center of the image
    screen[name] = [image_object, (image_coordinates[0] - image_object.get_width()/2, image_coordinates[1] - image_object.get_height()/2)]
    


def check_button_coords(coordinates: (int, int), button: dict) -> bool:
    """
    This function checks whether the given coordinates, <coordinates>, 
    are inside of a button object via the <button> dictionary, with respect 
    to the button's coordinates.
    """
    global WIDTH, HEIGHT 
    
    button_object = button[0]
    button_coordinates = button[1]

    BUTTON_WIDTH = button_object.get_width()
    BUTTON_HEIGHT = button_object.get_height()

    # Checks if the x-coordinates match
    if button_coordinates[0] <= coordinates[0] <= button_coordinates[0] + BUTTON_WIDTH:
        
        # Checks if the y-coordinates match
        if button_coordinates[1] <= coordinates[1] <= button_coordinates[1] + BUTTON_HEIGHT:
            return True  
    
    return False


def manage_music(volume: float=0.05):
    """
    By accessing the current screen that the user is on using the global variable 
    <SCREEN_STATUS>, manage what music is played and adjust its volume through the 
    <volume> parameter, which is defaulted to 0.25.
    """

    global SCREEN_STATUS, wave

    # Stop the previous music
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    # Access the music file PATH
    if SCREEN_STATUS == "MAIN":
        pygame.mixer.music.load("Music/main-menu-theme.mp3")
    if SCREEN_STATUS == "SHOP":
        pygame.mixer.music.load("Music/shop-theme.mp3")
    if SCREEN_STATUS == "FIGHT":
        pygame.mixer.music.load("Music/battle-theme-1.mp3")

    # Set the volume and play
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()


def main_menu():
    """
    Display the main menu in its entirety with all its text and images.
    """

    create_text("title", MAIN_MENU_TEXT, "Medieval Munchies", "Times New Roman", 64, (0, 0, 0), (540, 50))

    create_image("player", MAIN_MENU_IMAGES, player["sprite"], (225, 360), transparent=True, scaling=[600, 600])

    create_text("upgrade", MAIN_MENU_TEXT, "UPGRADE", "Times New Roman", 48, (219, 172, 52), (150+30, 630))
    create_image("upgrade", MAIN_MENU_IMAGES, "Images/anvil.png", (330+30, 635), transparent=True, scaling=[120, 120])
    
    create_text("fight", MAIN_MENU_TEXT, "FIGHT", "Times New Roman", 48, (255, 0, 0), (510+30, 630))
    create_image("fight", MAIN_MENU_IMAGES, "Images/carrot-sword.png", (660, 630), transparent=True, scaling=[80, 80])

    create_text("shop", MAIN_MENU_TEXT, "SHOP", "Times New Roman", 48, (17, 140, 79), (790+30, 630))
    create_image("shop", MAIN_MENU_IMAGES, "Images/shopping-cart.png", (900+30, 630), transparent=True, scaling=[80, 80])

    create_image("gold", MAIN_MENU_IMAGES, "Images/coin.png", (900,75), transparent=True, scaling=[100,100])
    create_text("gold_count", MAIN_MENU_TEXT, str(player['gold']), "Times New Roman", 48, (0, 0, 0), (975, 75))


def upgrade_menu(stats: list):
    """
    Given a list <stats> that contains elements in the format [name, path, coords, scale], 
    render each item to the upgrade menu.
    """

    global UPGRADE_MENU_TEXT, UPGRADE_MENU_IMAGES, WIDTH

    for i in range(len(stats)):
        create_image(
            stats[i][0], # Name 
            UPGRADE_MENU_IMAGES, # Location (Dictionary)
            stats[i][1], # Path
            (stats[i][2][0], stats[i][2][1]), # Coordinates
            transparent=True, # Transparency
            scaling=[stats[i][3][0], stats[i][3][1]] # Size
        )

        create_image(
            stats[i][0]+"_button", # Name 
            UPGRADE_MENU_IMAGES, # Location (Dictionary)
            "Images/plus.png", # Path
            (stats[i][2][0] + 200, stats[i][2][1]), # Coordinates
            transparent=True, # Transparency
            scaling=[stats[i][3][0]-100, stats[i][3][1]-100] # Size
        )
        
        create_text(
            stats[i][0]+"_desc", 
            UPGRADE_MENU_TEXT, 
            "cost: " + str(STATS_INFO[stats[i][0]]["cost"]),
            "Times New Roman", 
            48, 
            (0, 0, 0), 
            (stats[i][2][0]+350, stats[i][2][1])   
        )

    create_image("gold", UPGRADE_MENU_IMAGES, "Images/coin.png", (900,75), transparent=True, scaling=[100,100])
    create_image("upgrade_back", UPGRADE_MENU_IMAGES, "Images/arrow.png", (110, 80), transparent=True, scaling=[300, 300])
    create_image('training_dummy', UPGRADE_MENU_IMAGES, "Images/training_dummy.png", (800, 420), transparent=True, scaling=[400, 400])

def shop_menu(items: list):
    """
    Given a list <items> that contains elements in the format [name, path, coords, scale], 
    render each item to the shop menu.
    """

    global SHOP_MENU_TEXT, SHOP_MENU_IMAGES, WIDTH
    weapon_names = ["Chopsticks", "Spatula", "Knife", "Frying Pan"]

    for i in range(len(items)):
        create_image(
            items[i][0], # Name 
            SHOP_MENU_IMAGES, # Location (Dictionary)
            items[i][1], # Path
            (items[i][2][0], items[i][2][1]), # Coordinates
            transparent=True, # Transparency
            scaling=[items[i][3][0], items[i][3][1]] # Size
        )

        create_text(
            items[i][0]+"_desc", 
            SHOP_MENU_TEXT, 
            weapon_names[i] + ": $" + str(weapons[weapon_names[i]]["cost"]) + ", " + str(weapons[weapon_names[i]]["damage"]) + "dmg", 
            "Times New Roman", 
            30, 
            (0, 0, 0), 
            (items[i][2][0], items[i][2][1]-150)
        )

    create_image("gold", SHOP_MENU_IMAGES, "Images/coin.png", (900,75), transparent=True, scaling=[100,100])
    create_image("shop_back", SHOP_MENU_IMAGES, "Images/arrow.png", (110, 80), transparent=True, scaling=[300, 300])
    create_image("table", SHOP_MENU_IMAGES, "Images/shop-table.png", (540, 560), transparent=True, scaling=[650, 650])


def create_enemy(name: str, health: int, damage: int):
    TEMP_ENEMIES[name] = {"hp": health, "dmg": damage}


def tutorial_stage():

    global FIGHT_MENU_TEXT, FIGHT_MENU_IMAGES, TEMP_ENEMIES
    global player, wave

    FIGHT_MENU_TEXT = {}
    FIGHT_MENU_IMAGES = {}
    TEMP_ENEMIES = {}

    enemy_object = create_enemy("Dummy", 10, 0, "Images/amogus-ascended.png")
    TEMP_ENEMIES[enemy_object["name"]] = enemy_object 


def generate_enemy(last_enemy: dict) -> dict:
    """
    A function that generates a new enemy object, <random_enemy>,
    by scaling the stats based on the health and damage of the most recently
    fought enemy, <last_enemy>, with respect to the global scaling constants,
    <ENEMYHP_SCALING> and <ENEMYDMG_SCALING>.
    """
    
    global ENEMYHP_SCALING, ENEMYDMG_SCALING

    random_enemy = {}
    ENEMY_NAMES = ["Waiter", "Chef", "Farmer"]

    # Randomly chooses a basic enemy name and multiplies the hp and dmg of the enemy by a constant
    random_enemy['name'] = ENEMY_NAMES[randint(0, len(ENEMY_NAMES)-1)]
    random_enemy['hp'] = round((last_enemy['hp'] * ENEMYHP_SCALING), 2)
    random_enemy['dmg'] = round((last_enemy['dmg'] * ENEMYDMG_SCALING), 1)

    if random_enemy["name"] == "Waiter":
        random_enemy["sprite"] = "Images/waiter.png"
    if random_enemy["name"] == "Chef":
        random_enemy["sprite"] = "Images/chef.png"
    if random_enemy["name"] == "Farmer":
        random_enemy["sprite"] = "Images/farmer.png"

    return random_enemy


def random_event():
    """
    A function that creates random interactive events.
    """
    global completed_events, wave, SCREEN_STATUS
    
    number = randint(1,4)
    while number in completed_events:
        number = randint(1,4)
        
    completed_events.append(number)
    SCREEN_STATUS = "EVENT"
        
    """
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
        """
    
    """
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
    """

    return number


#---------------Game Loop---------------# 


def main():

    global SCREEN_STATUS, wave, weapons, player, in_boss_battle, FIGHT_MENU_TEXT
    global TEMP_ENEMIES, in_battle, in_event, BOSS_MOVEMENT_FACTOR
    global clock, last_frame, last_enemy, enemy_cooldown

    EVENT_MENU_TEXT = {}
    EVENT_MENU_IMAGES = {}
    
    ingredient = "Images/mystery.png"
    weapons = {
        "Chopsticks": {"cost": 5, "damage": 2},
        "Spatula": {"cost": 8, "damage": 3},
        "Knife": {"cost": 10, "damage": 4},
        "Frying Pan": {"cost": 12, "damage": 5}
    }
    
    # Initialize the game for the first playthrough
    SCREEN_STATUS = "TITLE"
    wave = 0
    screen_count = 1

    # TESTING (DELETE WHEN SUBMITTING)
    """
    wave = 14
    player['seasoned'] = True
    enemy_name = "Dummy"
    enemy_sprite = "Images/training_dummy.png"
    enemy_sprite_size = [400, 400] 
    create_enemy(enemy_name, 10, 1)
    last_enemy = enemy_name
    """

    # manage_music()

    # Initialize the images and text for each menu
    # via their respective functions
    main_menu()
    shop_menu([
                ["cs", "Images/chopsticks.png", (200, 320), [225,225]],
                ["sp", "Images/spatula.png", (415, 280), [335, 335]],
                ["kf", "Images/knife.png", (665, 280), [335,335]],
                ["fp", "Images/frying pan.png", (900, 320), [225,225]]

            ])
    upgrade_menu([
                ["health", "Images/heart.png", (100, 300), [200,200]],
                ["defence", "Images/shield.png", (100, 450), [200,200]],
                ["damage", "Images/sword.png", (100, 600), [200,200]],
            ])
        
    # Important flags and accumulators
    clicks = 0
    running = True


    # Actual Game Loop
    while running:

        # User Interfaces
        if SCREEN_STATUS == "TUTORIAL":
            TEXT = TUTORIAL_MENU_TEXT
            IMAGES = TUTORIAL_MENU_IMAGES

        if SCREEN_STATUS == "TITLE":
            TEXT = TITLE_MENU_TEXT
            IMAGES = TITLE_MENU_IMAGES

        if SCREEN_STATUS == "MAIN":
            TEXT = MAIN_MENU_TEXT
            IMAGES = MAIN_MENU_IMAGES

        elif SCREEN_STATUS == "SHOP":
            TEXT = SHOP_MENU_TEXT
            IMAGES = SHOP_MENU_IMAGES

        elif SCREEN_STATUS == "FIGHT":
            TEXT = FIGHT_MENU_TEXT
            IMAGES = FIGHT_MENU_IMAGES

        elif SCREEN_STATUS == "EVENT":
            TEXT = EVENT_MENU_TEXT
            IMAGES = EVENT_MENU_IMAGES
        
        elif SCREEN_STATUS == "UPGRADE":
            TEXT = UPGRADE_MENU_TEXT
            IMAGES = UPGRADE_MENU_IMAGES

        elif SCREEN_STATUS == "VICTORY":
            TEXT = VICTORY_MENU_TEXT
            IMAGES = VICTORY_MENU_IMAGES

        elif SCREEN_STATUS == "DEATH":
            TEXT = DEAD_MENU_TEXT
            IMAGES = DEAD_MENU_IMAGES

        elif SCREEN_STATUS == "ENDING":
            TEXT = GAME_ENDING_TEXT
            IMAGES = GAME_ENDING_IMAGES 


        # Track the (x, y) coordinates of the mouse
        # relative to the game window
        mouse_pos = pygame.mouse.get_pos()

        # Local Variables that aid in the instantiation 
        # of battle processes
        enemy_name = None
        enemy_sprite = None 
        enemy_sprite_size = None

        for event in pygame.event.get():

            # Closing the window ends the game
            if event.type == pygame.QUIT:
                running = False

            # This clause is to exclusively deal with random events
            if event.type == pygame.MOUSEBUTTONUP:
                if SCREEN_STATUS == "EVENT":
                    
                    if in_event == False:
                        first_screen = True
                        second_screen = False
                        ending_screen = False
                        stats_changed = False
                        ending = None
                        event_number = random_event()
                        in_event = True

                    # Runs the random event
                    if in_event == True:
                        
                        # Butcher Event
                        if event_number == 1:

                            # Loads the first screen
                            if first_screen == True:
                                EVENT_MENU_TEXT = {}
                                # Render the butcher sprite
                                create_text("enemy health", EVENT_MENU_TEXT, "BUTCHER APPROACHES", "Times New Roman", 64, (255, 0, 0), (540, 50))
                                create_image("butcher", EVENT_MENU_IMAGES, "Images/butcher.png", (810, 360), transparent=True, scaling=[400, 400])

                                # Text
                                create_text("dialogue 1", EVENT_MENU_TEXT, "Hey buddy, I need some help", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))
                                create_text("dialogue 2", EVENT_MENU_TEXT, "tenderizing my meat...", "Times New Roman", 48, (255, 0, 0), (250+100, 408-100))
                                create_text("dialogue 3", EVENT_MENU_TEXT, "Care to help?", "Times New Roman", 48, (255, 0, 0), (250+100, 456-100))
                                create_text("yes", EVENT_MENU_TEXT, "[Yes]", "Times New Roman", 48, (255, 0, 0), (250+100-100, 456-100+96))
                                create_text("no", EVENT_MENU_TEXT, "[No]", "Times New Roman", 48, (255, 0, 0), (250+100+100, 456-100+96))

                                # Identifies player decision
                                if check_button_coords(mouse_pos, EVENT_MENU_TEXT["yes"]) == True:
                                    # Goes straight to endings
                                    ending = 1
                                    ending_screen = True
                                    first_screen = False

                                elif check_button_coords(mouse_pos, EVENT_MENU_TEXT["no"]) == True:
                                    # Loads the second screen
                                    EVENT_MENU_TEXT = {}
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "How... Unfortunate.", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "I have another offer though.", "Times New Roman", 48, (255, 0, 0), (250+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "Can I buy your arm for 15 gold?", "Times New Roman", 48, (255, 0, 0), (250+100, 456-100))
                                    create_text("yes", EVENT_MENU_TEXT, "[Yes]", "Times New Roman", 48, (255, 0, 0), (100, 456-100+96))
                                    create_text("no", EVENT_MENU_TEXT, "[No]", "Times New Roman", 48, (255, 0, 0), (600, 456-100+96))  
                                    second_screen = True
                                    first_screen = False
                                    
                            # Checks for inputs on the second screen        
                            if second_screen == True:
                                if check_button_coords(mouse_pos, EVENT_MENU_TEXT["yes"]) == True:
                                    ending = 2
                                    second_screen = False
                                    ending_screen = True
                                
                                elif check_button_coords(mouse_pos, EVENT_MENU_TEXT["no"]) == True:
                                    ending = 3
                                    second_screen = False
                                    ending_screen = True

                            
                            # Displays a screen for each ending for the event
                            # Each has different stat changes
                            if ending_screen == True:
                                EVENT_MENU_TEXT = {}
                                if ending == 1:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "Thanks! You can start now!", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "He pays you, and you get stronger.", "Times New Roman", 48, (255, 0, 0), (250+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "+2 Gold, +1 Damage", "Times New Roman", 48, (255, 0, 0), (250+100, 456-100))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (250+100, 100))
                                    if stats_changed == False:
                                        player['gold'] += 2
                                        player['damage'] += 1
                                        stats_changed = True
                                elif ending == 2:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "Great!", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "I've always wanted...", "Times New Roman", 48, (255, 0, 0), (250+100, 308))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "...to try human meat.", "Times New Roman", 48, (255, 0, 0), (250+100, 358))                    
                                    create_text("dialogue 4", EVENT_MENU_TEXT, "+15 Gold, health & damage halved.", "Times New Roman", 36, (255, 0, 0), (250+100, 408))
                                    create_image("arm", EVENT_MENU_IMAGES, "Images/arm.png", (400, 560), transparent=True, scaling=[400, 400])
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (250+100, 100))
                                    if stats_changed == False:
                                        player['gold'] += 15
                                        player['damage'] //= 2
                                        player['health'] //= 2
                                        player['sprite'] = "Images/chef-character-armless.png"
                                        stats_changed = True
                                elif ending == 3:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "Alright, I'll see ya next time.", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))      
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (250+100, 100))                             
                                    
                        if event_number == 2:
                            if ending_screen == False:
                                create_text("enemy health", EVENT_MENU_TEXT, "FOOD MARKET", "Times New Roman", 64, (255, 0, 0), (540, 50))
                                create_text("dialogue 1", EVENT_MENU_TEXT, "You can buy one item for free...", "Times New Roman", 40, (255, 0, 0), (540, 150))
                                create_image("chicken", EVENT_MENU_IMAGES, "Images/chicken.png", (200, 360), transparent=True, scaling=[200, 200])
                                create_image("milk", EVENT_MENU_IMAGES, "Images/milk.png", (400, 360), transparent=True, scaling=[200, 200])
                                create_image("rice", EVENT_MENU_IMAGES, "Images/rice.png", (600, 360), transparent=True, scaling=[200, 200])
                                create_image("chili", EVENT_MENU_IMAGES, "Images/chili.png", (800, 360), transparent=True, scaling=[200, 200])
                                create_text("leave", EVENT_MENU_TEXT, "Leave", "Times New Roman", 64, (0,0,0), (500, 500))
                                if check_button_coords(mouse_pos, EVENT_MENU_IMAGES["chicken"]) == True:  
                                    ending = 1
                                    ending_screen = True
                                elif check_button_coords(mouse_pos, EVENT_MENU_IMAGES["milk"]) == True:
                                    ending = 2
                                    ending_screen = True
                                elif check_button_coords(mouse_pos, EVENT_MENU_IMAGES["rice"]) == True:
                                    ending = 3
                                    ending_screen = True
                                elif check_button_coords(mouse_pos, EVENT_MENU_IMAGES["chili"]) == True:
                                    ending = 4
                                    ending_screen = True
                                elif check_button_coords(mouse_pos, EVENT_MENU_TEXT["leave"]) == True:
                                    ending = 5
                                    ending_screen = True
                                
                            if ending_screen == True:
                                EVENT_MENU_TEXT = {}
                                EVENT_MENU_IMAGES = {}
                                if ending == 1:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "You consume the chicken...", 48, (255, 0, 0), (440+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "Why would you choose the unhealthiest item?", "Times New Roman", 36, (255, 0, 0), (440+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "-2 Health", "Times New Roman", 48, (255, 0, 0), (440+100, 456-100))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100))
                                    if stats_changed == False:
                                        player['health'] -= 2
                                        stats_changed = True
                                elif ending == 2:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "You consume the milk...", "Times New Roman", 48, (255, 0, 0), (440+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "It strengthens your bones!", "Times New Roman", 48, (255, 0, 0), (440+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "+1 Defence", "Times New Roman", 48, (255, 0, 0), (440+100, 456-100))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100))
                                    if stats_changed == False:
                                        player['defence'] += 1
                                        stats_changed = True
                                elif ending == 3:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "You consumed the rice...", "Times New Roman", 48, (255, 0, 0), (440+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "It gives you the calories you need!", "Times New Roman", 48, (255, 0, 0), (440+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "+4 Health", "Times New Roman", 48, (255, 0, 0), (440+100, 456-100))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100))
                                    if stats_changed == False:                          
                                        player['health'] += 4
                                        stats_changed = True
                                elif ending == 4:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "You consume the chili...", "Times New Roman", 48, (255, 0, 0), (440+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "The spice boosts your physical ability...", "Times New Roman", 48, (255, 0, 0), (440+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "+1 Damage", "Times New Roman", 48, (255, 0, 0), (440+100, 456-100))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100))
                                    if stats_changed == False:
                                        player['damage'] += 1
                                        stats_changed = True
                                elif ending == 5:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "You leave the market.", "Times New Roman", 48, (255, 0, 0), (440+100, 360-100))      
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100))                           
                            
                                
                        if event_number == 3:
                            if ending_screen == False:
                                create_text("enemy health", EVENT_MENU_TEXT, "You find a stash of 11 herbs and spices...", "Times New Roman", 48, (255, 0, 0), (540, 50))
                                create_text("dialogue 1", EVENT_MENU_TEXT, "Do you consume the spices or keep them?", "Times New Roman", 48, (255, 0, 0), (540, 600)) 
                                create_image("spices", EVENT_MENU_IMAGES, "Images/spices-herbs.png", (540, 300), transparent=True, scaling=[450,450])
                                create_text("yes", EVENT_MENU_TEXT, "[yes]", "Times New Roman", 48, (255, 0, 0), (300, 650))   
                                create_text("no", EVENT_MENU_TEXT, "[no]", "Times New Roman", 48, (255, 0, 0), (780, 650))                          
                                if check_button_coords(mouse_pos, EVENT_MENU_TEXT["yes"]) == True:
                                    ending = 1
                                    ending_screen = True
                                elif check_button_coords(mouse_pos, EVENT_MENU_TEXT["no"]) == True:
                                    ending = 2
                                    ending_screen = True
                                    
                            if ending_screen == True:
                                EVENT_MENU_TEXT = {}
                                EVENT_MENU_IMAGES = {}
                                if ending == 1:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "You straight up consume", "Times New Roman", 48, (255, 0, 0), (440+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "all of the spices...", "Times New Roman", 36, (255, 0, 0), (440+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "+3 Damage, -4 Health", "Times New Roman", 36, (255, 0, 0), (440+100, 456-100))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100)) 
                                    if stats_changed == False:
                                        player['health'] -= 4
                                        player['damage'] += 3
                                        stats_changed = True
                                if ending == 2:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "You keep the spices for some reason...", "Times New Roman", 48, (255, 0, 0), (440+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "There is a [COLONEL] sticker on the bottom...", "Times New Roman", 36, (255, 0, 0), (440+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "You put the spices in your backpack.", "Times New Roman", 36, (255, 0, 0), (440+100, 456-100))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100))     
                                    player['seasoned'] = True          
                                    
                        if event_number == 4:
                            if first_screen == True:
                                create_text("enemy health", EVENT_MENU_TEXT, "You find a covered plate...", "Times New Roman", 64, (255, 0, 0), (540, 50))
                                create_text("dialogue 1", EVENT_MENU_TEXT, "Do you want to", "Times New Roman", 48, (255, 0, 0), (440+100, 500))
                                create_text("dialogue 2", EVENT_MENU_TEXT, "take what's inside or get a new plate?", "Times New Roman", 48, (255, 0, 0), (440+100, 550))
                                create_text("dialogue 3", EVENT_MENU_TEXT, "(This action is irreversible.)", "Times New Roman", 48, (255, 0, 0), (540, 600))
                                create_text("yes", EVENT_MENU_TEXT, "[yes]", "Times New Roman", 48, (255, 0, 0), (400, 650))   
                                create_text("no", EVENT_MENU_TEXT, "[no]", "Times New Roman", 48, (255, 0, 0), (680, 650))    
                                create_image("plate_1", EVENT_MENU_IMAGES, "Images/covered-dish.png", (540, 275), transparent=True, scaling=[600,600])      

                                if check_button_coords(mouse_pos, EVENT_MENU_TEXT["yes"]) == True:
                                    ending = 1
                                    first_screen = False
                                    ending_screen = True
                                elif check_button_coords(mouse_pos, EVENT_MENU_TEXT["no"]) == True:
                                    first_screen = False
                                    second_screen = True
                                    
                            if second_screen == True:
                                EVENT_MENU_IMAGES = {}
                                EVENT_MENU_TEXT = {}
                                create_text("enemy health", EVENT_MENU_TEXT, "You swap plates...", "Times New Roman", 64, (255, 0, 0), (540, 50))
                                create_image("plate_2", EVENT_MENU_IMAGES, "Images/covered-dish-2.png", (540, 275), transparent=True, scaling=[600, 600])
                                create_text("dialogue 1", EVENT_MENU_TEXT, "Do you want to", "Times New Roman", 48, (255, 0, 0), (440+100, 550))
                                create_text("dialogue 2", EVENT_MENU_TEXT, "take what's inside this plate?", "Times New Roman", 48, (255, 0, 0), (440+100, 600))
                                create_text("yes", EVENT_MENU_TEXT, "[yes]", "Times New Roman", 48, (255, 0, 0), (250, 650))   
                                create_text("no", EVENT_MENU_TEXT, "[no]", "Times New Roman", 48, (255, 0, 0), (830, 650))    

                                if check_button_coords(mouse_pos, EVENT_MENU_TEXT["yes"]) == True:
                                    ending = 2
                                    ending_screen = True
                                    second_screen = False
                                elif check_button_coords(mouse_pos, EVENT_MENU_TEXT["no"]) == True:
                                    ending = 3
                                    ending_screen = True
                                    second_screen = False
                                
                            if ending_screen == True:
                                EVENT_MENU_IMAGES = {}
                                EVENT_MENU_TEXT = {}
                                if ending == 1:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "There was a...", "Times New Roman", 48, (255, 0, 0), (440+100, 500))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "knife sharpener inside!", "Times New Roman", 48, (255, 0, 0), (440+100, 550))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "+2 Damage", "Times New Roman", 48, (255, 0, 0), (540, 600)) 
                                    create_image("plate_1", EVENT_MENU_IMAGES, "Images/dish-knife-sharpener.png", (540, 275), transparent=True, scaling=[500,500])  
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100))
                                    if stats_changed == False:
                                        player['damage'] += 2
                                        stats_changed = True
                                        
                                elif ending == 2:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "There was a...", "Times New Roman", 48, (255, 0, 0), (440+100, 500))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "glass of water inside...", "Times New Roman", 48, (255, 0, 0), (440+100, 550))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "You drink it and nothing happens.", "Times New Roman", 48, (255, 0, 0), (540, 600)) 
                                    create_image("plate_1", EVENT_MENU_IMAGES, "Images/dish-glass-water.png", (540, 275), transparent=True, scaling=[500,500]) 
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 100))                           
                                elif ending == 3:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "You just leave.", "Times New Roman", 48, (255, 0, 0), (440+100, 600))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 60, (255, 0, 0), (440+100, 300))  

                        try:
                            if check_button_coords(mouse_pos, EVENT_MENU_TEXT["continue"]) == True:
                                in_event = False
                                SCREEN_STATUS = "MAIN"
                                EVENT_MENU_IMAGES = {}
                                EVENT_MENU_TEXT = {}
                                wave += 1    
                        except KeyError:
                            pass
                            
            # Title Screen and Tutorial Sequence
            if SCREEN_STATUS == "TITLE":
                WIN.fill((255, 255, 255))
                create_text("title", TITLE_MENU_TEXT, "MEDIEVAL MUNCHIES", "Times New Roman", 64, (0, 0, 0), (540, 200+50))
                create_text("start", TITLE_MENU_TEXT, "[START]", "Times New Roman", 64, (0, 255, 0), (540-64*3, 360+50))
                create_text("quit", TITLE_MENU_TEXT, "[QUIT]", "Times New Roman", 64, (255, 0, 0), (540+64*3, 360+50))


            # Mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                if SCREEN_STATUS == "TITLE":
                    
                    if check_button_coords(mouse_pos, TITLE_MENU_TEXT["start"]):
                        SCREEN_STATUS = "TUTORIAL" 
                        create_text("1", TUTORIAL_MENU_TEXT, "You are a Chef for the Banjevic Aristocracy.", "Times New Roman", 36, (0, 0, 0), (540, 50))
                        create_text("2", TUTORIAL_MENU_TEXT, "King Banjevic has decreed you to bake him a cake for his birthday.", "Times New Roman", 36, (0, 0, 0), (540, 50+48*2))   
                        create_text("3", TUTORIAL_MENU_TEXT, "(Everyone keeps forgetting...)", "Times New Roman", 36, (0, 0, 0), (540, 50+48*4))   
                        create_text("4", TUTORIAL_MENU_TEXT, "Alas, what are thee to do but listen?", "Times New Roman", 36, (0, 0, 0), (540, 50+48*6))   
                        create_text("5", TUTORIAL_MENU_TEXT, "Go, gather ingredients, and conquer the world!", "Times New Roman", 36, (0, 0, 0), (540, 50+48*8))
                        create_text("6", TUTORIAL_MENU_TEXT, ">> Click Here to Start <<", "Times New Roman", 36, (255, 0, 0), (540, 600))
                        create_image("7", TUTORIAL_MENU_IMAGES, "Images/good-luck.png", (900, 600), transparent=True, scaling=[200,200]) 

                    
                    if check_button_coords(mouse_pos, TITLE_MENU_TEXT["quit"]):
                        running = False

                
                if SCREEN_STATUS == "TUTORIAL":
                    
                    if check_button_coords(mouse_pos, TUTORIAL_MENU_TEXT["6"]):
                        wave = 0
                        SCREEN_STATUS = "FIGHT"


                if SCREEN_STATUS == "UPGRADE":
                    upgrade_choice = None

                    if check_button_coords(mouse_pos, UPGRADE_MENU_IMAGES["upgrade_back"]) == True:
                        SCREEN_STATUS = "MAIN"
                    elif check_button_coords(mouse_pos, UPGRADE_MENU_IMAGES["health_button"]) == True:
                        upgrade_choice = "health"
                    elif check_button_coords(mouse_pos, UPGRADE_MENU_IMAGES["defence_button"]) == True:
                        upgrade_choice = "defence"
                    elif check_button_coords(mouse_pos, UPGRADE_MENU_IMAGES["damage_button"]) == True:
                        upgrade_choice = "damage"

                    if upgrade_choice in player.keys():
                        if player["gold"] >= STATS_INFO[upgrade_choice]["cost"]:
                            if upgrade_choice == "defence":
                                if player["defence"] >= STATS_INFO['defence']['max']:
                                    create_text("upgrade_note", UPGRADE_MENU_TEXT, "Defence is maxed!", "Times New Roman", 48, (0, 0, 0), (540, 75))
                                else:
                                    player[upgrade_choice] += STATS_INFO[upgrade_choice]['increment']
                                    player["gold"] -= STATS_INFO[upgrade_choice]['cost']
                                    create_text("upgrade_note", UPGRADE_MENU_TEXT, "You upgraded: " + upgrade_choice, "Times New Roman", 48, (0, 0, 0), (540, 75))    
                            else:
                                player[upgrade_choice] += STATS_INFO[upgrade_choice]['increment']
                                player["gold"] -= STATS_INFO[upgrade_choice]['cost']
                                create_text("upgrade_note", UPGRADE_MENU_TEXT, "You upgraded: " + upgrade_choice, "Times New Roman", 48, (0, 0, 0), (540, 75))   
                
                        else:
                            create_text("upgrade_note", UPGRADE_MENU_TEXT, "You don't have enough gold!", "Times New Roman", 48, (0, 0, 0), (540, 75))                           


                # Function for each menu
                if SCREEN_STATUS == "MAIN":
                    if check_button_coords(mouse_pos, MAIN_MENU_TEXT["fight"]) == True or check_button_coords(mouse_pos, MAIN_MENU_IMAGES["fight"]) == True:
                        SCREEN_STATUS = "FIGHT"
                    elif check_button_coords(mouse_pos, MAIN_MENU_TEXT["shop"]) == True or check_button_coords(mouse_pos, MAIN_MENU_IMAGES["shop"]) == True:
                        SCREEN_STATUS = "SHOP"
                    elif check_button_coords(mouse_pos, MAIN_MENU_TEXT["upgrade"]) == True or check_button_coords(mouse_pos, MAIN_MENU_IMAGES["upgrade"]) == True:
                        SCREEN_STATUS = "UPGRADE"

                if wave <= 20:
                    if SCREEN_STATUS == "FIGHT":

                        print(enemy_cooldown)

                        if wave == 0:
                            enemy_name = "Dummy"
                            enemy_sprite = "Images/training_dummy.png"
                            enemy_sprite_size = [400, 400] 
                            create_enemy(enemy_name, 10, 1)
                        
                        elif wave % 5 == 0:

                            if wave == 5:
                                enemy_name = "Burger King"
                                enemy_sprite = "Images/burger_king.png"
                                ingredient = "Images/egg.png"
                                enemy_sprite_size = [500, 500]
                                create_enemy(enemy_name, 20, 2)
                                in_boss_battle = True
                            
                            if wave == 10:
                                enemy_name = "Ronald McDonald"
                                enemy_sprite = "Images/ronald.png"
                                ingredient = "Images/butter.png"
                                enemy_sprite_size = [500, 500]
                                create_enemy(enemy_name, 20, 2)
                                in_boss_battle = True

                            if wave == 15:
                                enemy_name = "Colonel Sanders"
                                enemy_sprite = "Images/colonel.png"
                                ingredient = "Images/flour.png"
                                enemy_sprite_size = [500, 500]
                                create_enemy(enemy_name, 20, 2)
                                in_boss_battle = True

                            if wave == 20:
                                enemy_name = "Gordon Ramsay"
                                enemy_sprite = "Images/gordon.png"
                                ingredient = "Images/sugar.png"
                                enemy_sprite_size = [500, 500]
                                create_enemy(enemy_name, 20, 2)
                                in_boss_battle = True

                        elif wave % 10 == 3 or wave % 10 == 8:

                            # Switch to event screen
                            SCREEN_STATUS = "EVENT"

                        else:
                            
                            # Only generate a new enemy
                            # if the battle process is not 
                            # currently running
                            if in_battle == False:
                                new_enemy = generate_enemy(TEMP_ENEMIES[last_enemy])
                            
                            enemy_name = new_enemy["name"]
                            enemy_sprite = new_enemy["sprite"]
                            enemy_sprite_size = [400, 400]
                            create_enemy(enemy_name, new_enemy["hp"], new_enemy["dmg"])
                            
                        # Battle process
                        # Ensures that an event has not been triggered,
                        # by checking the SCREEN_STATUS
                        if SCREEN_STATUS == "FIGHT":

                            # If the player has died in battle
                            if in_battle == True and round(player_hp) <= 0:

                                # Reset the Death menus
                                DEAD_MENU_TEXT = {}
                                DEAD_MENU_IMAGES = {}

                                # End the battle process
                                in_battle = False
                                wave += 1
                                last_enemy = enemy_name
                                            
                                # End the boss battle, if applicable
                                if in_boss_battle == True:
                                    in_boss_battle = False

                                SCREEN_STATUS = "DEATH"
                                last_enemy = enemy_name
                                
                                WIN.fill((0, 0, 0))
                                
                                # Death Menu Text 
                                create_text("game over", DEAD_MENU_TEXT, f'YOU DIED TO {last_enemy.upper()}, BUT', "Times New Roman", 48, (255, 255, 255), (540, 300-75))
                                create_text("heroes never die", DEAD_MENU_TEXT, f'THEY SAY THAT HEROES NEVER DIE...', "Times New Roman", 48, (255, 255, 255), (540, 350-75))
                                create_text("try again", DEAD_MENU_TEXT, f'Try again?', "Times New Roman", 48, (255, 0, 0), (540, 450-75))
                                create_text("yes", DEAD_MENU_TEXT, '[Yes]', "Times New Roman", 48, (255, 255, 255), (540-48*2, 550-75))
                                create_text("no", DEAD_MENU_TEXT, '[No]', "Times New Roman", 48, (255, 255, 255), (540+48*2, 550-75))
                        
                            if in_battle == False:
                                    
                                # Reset the menu images and text
                                FIGHT_MENU_IMAGES = {}
                                FIGHT_MENU_TEXT = {}

                                # Render the enemy sprite
                                create_image(enemy_name, FIGHT_MENU_IMAGES, enemy_sprite, (540, 360), transparent=True, scaling=enemy_sprite_size)

                                # Create temporary variables for the battle
                                player_hp = player["health"]

                                enemy_hp = TEMP_ENEMIES[enemy_name]["hp"]
                                enemy_dmg = TEMP_ENEMIES[enemy_name]["dmg"]
                                print(enemy_dmg)

                                # Render the enemy health and player health, defense, attack stats
                                create_text("enemy health", FIGHT_MENU_TEXT, f"{enemy_name.upper()} APPROACHES", "Times New Roman", 64, (255, 0, 0), (540, 50))

                                # Extra tutorial text
                                if wave == 0:
                                    create_text("tutorial_clicks", FIGHT_MENU_TEXT, "← Click on me!", "Times New Roman", 48, (0, 0, 0), (825, 225))

                                create_image("player health", FIGHT_MENU_IMAGES, "Images/heart.png", (805, 680), transparent=True, scaling=[75,75])
                                create_text("player health", FIGHT_MENU_TEXT, f"Health: {player_hp}", "Times New Roman", 48, (0, 0, 0), (950, 675))

                                create_text("player defense", FIGHT_MENU_TEXT, f"Defense: {player['defence']}", "Times New Roman", 48, (0, 0, 0), (540, 675))
                                
                                create_text("player damage", FIGHT_MENU_TEXT, f"Damage: {player['damage'] * player['weapon_multiplier']}", "Times New Roman", 48, (0, 0, 0), (150, 675))
                                    
                                # Begin the Battle Loop
                                in_battle = True
                                enemy_cooldown = 0
                                print(f"Enemy Health: {enemy_hp}")

                                
                            else:

                                # Increment the cooldown with respect
                                # to the frame rate of the game
                                enemy_cooldown += last_frame

                                # If the cooldown has reached <arbitrary value>, 
                                # deal damage to the player
                                if enemy_cooldown > 2 * last_frame: 
                                    enemy_cooldown = 0
                                    player_hp = round(player_hp - (enemy_dmg * (1 - player["defence"]/10)), 2)
                                    
                                    # Boss Functionalities
                                    if in_boss_battle == True:
                                        
                                        # Allows the enemy to teleport across the map 
                                        # while it deals damage
                                        new_coordinates = (randint(500, 580), randint(300, 420) * BOSS_MOVEMENT_FACTOR)
                                    
                                        # Re-render the image
                                        create_image(enemy_name, FIGHT_MENU_IMAGES, enemy_sprite, new_coordinates, transparent=True, scaling=enemy_sprite_size)

                                # Check if the enemy has been clicked
                                if check_button_coords(mouse_pos, FIGHT_MENU_IMAGES[enemy_name]) == True:

                                    if wave == 0:
                                        create_text("tutorial_health", FIGHT_MENU_TEXT, "My health!!!", "Times New Roman", 48, (255, 0, 0), (300, 225))
                                        
                                    # Damage calculations
                                    player_damage = player['damage'] * player['weapon_multiplier']
                                    enemy_hp -= player_damage

                                    print(f"\nYou did {player_damage} damage!")
                                    print(f"Enemy Health: {enemy_hp}")
                                    print(f"Your Health: {player_hp}")

                                    # Wins the battle when the enemy health is 0
                                    if enemy_hp <= 0:

                                        # Enemy Dies
                                        if round(enemy_hp) <= 0:
                                            
                                            # Reset the Victory and Loss menus
                                            VICTORY_MENU_TEXT = {}
                                            VICTORY_MENU_IMAGES = {}

                                            print("VICTORY")
                                            enemy_hp = 0
                                                    
                                            create_text("slain", VICTORY_MENU_TEXT, f'YOU HAVE SLAIN {enemy_name.upper()}', "Times New Roman", 60, (0, 0, 0), (540, 150))
                                            create_text("continue", VICTORY_MENU_TEXT, f'>> Click Here to Continue <<', "Times New Roman", 48, (255, 0, 0), (540, 250))

                                            SCREEN_STATUS = "VICTORY"

                                            # End the battle process
                                            player['gold'] += 1
                                            in_battle = False
                                            wave += 1
                                            last_enemy = enemy_name
                                            
                                            # End the boss battle, if applicable
                                            if in_boss_battle == True:
                                                create_text("dialogue 1", VICTORY_MENU_TEXT, "But wait...", "Times New Roman", 48, (0, 0, 0), (540, 225))
                                                create_text("dialogue 2", VICTORY_MENU_TEXT, "...The boss drops an ingredient...", "Times New Roman", 48, (0, 0, 0), (540, 290))
                                                create_image("ingredient", VICTORY_MENU_IMAGES, ingredient, (540, 460), transparent=True, scaling=[300,300])
                                                create_text("continue", VICTORY_MENU_TEXT, f'>> Click Here to Continue <<', "Times New Roman", 48, (255, 0, 0), (540, 650))
                                                if wave == 6:  
                                                    player['egg'] = ingredient
                                                elif wave == 11:
                                                    player['butter'] = ingredient
                                                elif wave == 16:
                                                    player['flour'] = ingredient
                                                    
                                                    # Secret Colonel Questline + Ending
                                                    if player['seasoned'] == True:
                                                        create_text("dialogue1", VICTORY_MENU_TEXT, 'He noticed that you have', "Times New Roman", 24, (255, 0, 0), (200, 400-50))
                                                        create_text("dialogue2", VICTORY_MENU_TEXT, 'his 11 herbs and spices...', "Times New Roman", 24, (255, 0, 0), (200, 425-50))
                                                        create_text("dialogue3", VICTORY_MENU_TEXT, 'The Colonel hands you...', "Times New Roman", 24, (255, 0, 0), (200, 450-50))
                                                        create_text("dialogue4", VICTORY_MENU_TEXT, 'a bucket of chicken!', "Times New Roman", 24, (255, 0, 0), (200, 475-50))
                                                        create_image("chicken bucket", VICTORY_MENU_IMAGES, "Images/chicken-bucket.png", (200,600-80), transparent=True, scaling=[200,200])                   
                                                        player['chicken'] = True

                                                elif wave == 21:
                                                    player['sugar'] = ingredient
                                                in_boss_battle = False


                                # Update the enemy and player health text
                                # Floor and round each value to avoid floating point errors
                                create_text("player health", FIGHT_MENU_TEXT, f"Health: {round(player_hp)}", "Times New Roman", 48, (0, 0, 0), (950, 675))
                                create_text("enemy health", FIGHT_MENU_TEXT, f"Health: {ceil(enemy_hp)}", "Times New Roman", 64, (255, 0, 0), (540, 50))

                elif wave > 20:
                    SCREEN_STATUS = "ENDING"

                if SCREEN_STATUS == "VICTORY":
                    
                    # If you are on the victory screen,
                    # allow the continue button to switch to
                    # the main menu

                    # Displays ingredient if after a boss wave

                    if check_button_coords(mouse_pos, VICTORY_MENU_TEXT["continue"]):
                        SCREEN_STATUS = "MAIN"
                

                elif SCREEN_STATUS == "DEATH":

                    # Restart the game 
                    if check_button_coords(mouse_pos, DEAD_MENU_TEXT["yes"]):
                        SCREEN_STATUS = "MAIN"
                        wave = 0

                        player = {
                            "health": 10, 
                            "damage": 1, 
                            "defence": 0, 
                            "gold": 100, 
                            
                            # The spoon has a damage of 1
                            "weapon": "Spoon",

                            # weapon multiplier = 1 + (weapon_damage - 1)/4
                            "weapon_multiplier": 1,
                            
                            "weapon_image": "Images/spoon.png",
                            'seasoned': False, 
                            "chicken": False,
                            "sprite": "Images/chef-character.png",

                            'egg': "Images/mystery.png",
                            'butter': "Images/mystery.png",
                            'flour': "Images/mystery.png",
                            'sugar': "Images/mystery.png"
                        }


                        enemy_name = "Dummy"
                        enemy_sprite = "Images/training_dummy.png"
                        enemy_sprite_size = [400, 400] 
                        create_enemy(enemy_name, 10, 1)
                    
                    # Close the game
                    if check_button_coords(mouse_pos, DEAD_MENU_TEXT["no"]):
                        running = False


                elif SCREEN_STATUS == "SHOP":
                    shop_choice = None
                    if check_button_coords(mouse_pos, SHOP_MENU_IMAGES["shop_back"]) == True:
                        SCREEN_STATUS = "MAIN"

                    if check_button_coords(mouse_pos, SHOP_MENU_IMAGES["cs"]) == True:
                        shop_choice = "Chopsticks"
                    if check_button_coords(mouse_pos, SHOP_MENU_IMAGES["sp"]) == True:
                        shop_choice = "Spatula"
                    if check_button_coords(mouse_pos, SHOP_MENU_IMAGES["kf"]) == True:
                        shop_choice = "Knife"
                    if check_button_coords(mouse_pos, SHOP_MENU_IMAGES["fp"]) == True:
                        shop_choice = "Frying Pan"

                    if shop_choice in weapons.keys():
                        if weapons[shop_choice]["cost"] == "SOLD :(":
                            create_text("buy_note", SHOP_MENU_TEXT, "You already bought: " + shop_choice, "Times New Roman", 36, (0, 0, 0), (540, 75))
                        elif player['gold'] < weapons[shop_choice]["cost"]:
                            create_text("buy_note", SHOP_MENU_TEXT, "You cannot afford to buy: " + shop_choice, "Times New Roman", 36, (0, 0, 0), (540, 75))
                        else:    
                            player["weapon"] = shop_choice
                            player['weapon_image'] = "Images/" + shop_choice.lower() + ".png"
                            player['gold'] -= weapons[shop_choice]["cost"]
                            player["weapon_multiplier"] = 1 + (weapons[shop_choice]["damage"] - 1)/4
                            weapons[shop_choice]["cost"] = "SOLD :("
                            create_text("buy_note", SHOP_MENU_TEXT, "You successfully bought: " + shop_choice, "Times New Roman", 36, (0, 0, 0), (540, 75))

                elif SCREEN_STATUS == "ENDING":

                    if screen_count == 1:
                        GAME_ENDING_IMAGES = {}
                        GAME_ENDING_TEXT = {}
                        create_text("enemy health", GAME_ENDING_TEXT, "You collected all four ingredients!!", "Times New Roman", 64, (255, 0, 0), (540, 550))
                        create_text("dialogue 1", GAME_ENDING_TEXT, "Bake to impress Mr. Banjevic!", "Times New Roman", 48, (255, 0, 0), (440+100, 625))
                        create_text("continue", GAME_ENDING_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 50))

                        create_image("egg", GAME_ENDING_IMAGES, "Images/egg.png", (400, 200), transparent=True, scaling=[250,250])
                        create_image("butter", GAME_ENDING_IMAGES, "Images/butter.png", (680, 200), transparent=True, scaling=[250,250])
                        create_image("flour", GAME_ENDING_IMAGES, "Images/flour.png", (400, 415), transparent=True, scaling=[250,250])
                        create_image("sugar", GAME_ENDING_IMAGES, "Images/sugar.png", (680, 415), transparent=True, scaling=[250,250])
                        
                        if check_button_coords(mouse_pos, GAME_ENDING_TEXT["continue"]) == True:
                            screen_count += 1

                    if screen_count == 2:
                        GAME_ENDING_IMAGES = {}
                        GAME_ENDING_TEXT = {}
                        create_text("enemy health", GAME_ENDING_TEXT, "You baked this cake!", "Times New Roman", 64, (255, 0, 0), (540, 50))
                        if player['chicken'] == False:
                            create_image("cake", GAME_ENDING_IMAGES, "Images/cake.png", (540, 360), transparent=True, scaling=[400,400])    
                            create_text("dialogue 1", GAME_ENDING_TEXT, "Proceed to give it to Mr. Banjevic!", "Times New Roman", 48, (255, 0, 0), (440+100, 550))
                            create_text("continue", GAME_ENDING_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (440+100, 625))
                            if check_button_coords(mouse_pos, GAME_ENDING_TEXT["continue"]) == True:
                                screen_count += 1

                        elif player['chicken'] == True:
                            create_text("dialogue 1", GAME_ENDING_TEXT, "You were gonna give Mr. Banjevic the cake but...", "Times New Roman", 48, (255, 0, 0), (440+100, 120))
                            create_text("dialogue 2", GAME_ENDING_TEXT, "You remembered that you also had the Colonel's chicken.", "Times New Roman", 36, (255, 0, 0), (440+100, 170))
                            create_text("dialogue 3", GAME_ENDING_TEXT, "Which one do you choose?", "Times New Roman", 36, (255, 0, 0), (440+100, 220))
                            
                            create_image("cake", GAME_ENDING_IMAGES, "Images/cake.png", (300, 500), transparent=True, scaling=[400,400])  
                            create_image("chicken-bucket", GAME_ENDING_IMAGES, "Images/chicken-bucket.png", (780, 500), transparent=True, scaling=[400,400])  
                            if check_button_coords(mouse_pos, GAME_ENDING_IMAGES["cake"]) == True:
                                screen_count += 1
                            if check_button_coords(mouse_pos, GAME_ENDING_IMAGES["chicken-bucket"]) == True:
                                screen_count += 2

                    if screen_count == 3:
                        GAME_ENDING_IMAGES = {}
                        GAME_ENDING_TEXT = {}
                        create_text("ending name", GAME_ENDING_TEXT, "--- CAKE ENDING ---", "Times New Roman", 64, (255, 0, 0), (540, 50))
                        create_text("dialogue 1", GAME_ENDING_TEXT, "Mr. Banjevic gives the cake a... ", "Times New Roman", 48, (255, 0, 0), (440+100, 120))
                        create_text("dialogue 2", GAME_ENDING_TEXT, "9/10!", "Times New Roman", 80, (255, 0, 0), (440+100, 200))
                        create_image("cake", GAME_ENDING_IMAGES, "Images/cake.png", (540, 430), transparent=True, scaling=[400,400])    

                    if screen_count == 4:
                        GAME_ENDING_IMAGES = {}
                        GAME_ENDING_TEXT = {}
                        create_text("ending name", GAME_ENDING_TEXT, "--- COLONEL'S CHICKEN ENDING ---", "Times New Roman", 64, (255, 0, 0), (540, 50))
                        create_text("dialogue 1", GAME_ENDING_TEXT, "Mr. Banjevic gives the Colonel's Chicken a... ", "Times New Roman", 48, (255, 0, 0), (440+100, 120))
                        create_text("dialogue 2", GAME_ENDING_TEXT, "10/10!", "Times New Roman", 80, (255, 0, 0), (440+100, 200))
                        create_image("chicken-bucket", GAME_ENDING_IMAGES, "Images/chicken-bucket.png", (540, 430), transparent=True, scaling=[400,400])   

            # Updating main menu info (player stats)
            # Updating player sprite
            create_image("player", MAIN_MENU_IMAGES, player["sprite"], (225, 360), transparent=True, scaling=[600, 600])

            # Gold count
            create_text("gold_count", MAIN_MENU_TEXT, str(player['gold']), "Times New Roman", 48, (0, 0, 0), (975, 75))
            create_text("gold_count", UPGRADE_MENU_TEXT, str(player['gold']), "Times New Roman", 48, (0, 0, 0), (975, 75))
            create_text("gold_count", SHOP_MENU_TEXT, str(player['gold']), "Times New Roman", 48, (0, 0, 0), (975, 75)) 

            # Base stats
            create_image("heart", MAIN_MENU_IMAGES, "Images/heart.png", (900, 170), transparent=True, scaling=[100, 100])
            create_image("shield", MAIN_MENU_IMAGES, "Images/shield.png", (900, 245), transparent=True, scaling=[100, 100])
            create_image("sword", MAIN_MENU_IMAGES, "Images/sword.png", (900, 320), transparent=True, scaling=[100, 100])
            create_text("hp_stat", MAIN_MENU_TEXT, str(player['health']), "Times New Roman", 48, (0, 0, 0), (975, 170))
            create_text("def_stat", MAIN_MENU_TEXT, str(player['defence']), "Times New Roman", 48, (0, 0, 0), (975, 245))
            create_text("dmg_stat", MAIN_MENU_TEXT, str(player['damage']), "Times New Roman", 48, (0, 0, 0), (975, 320))

            # Collected ingredients
            create_text('ingredients', MAIN_MENU_TEXT, "Ingredients:", "Times New Roman", 48, (0, 0, 0), (925, 385))
            create_image("egg", MAIN_MENU_IMAGES, player['egg'], (800+75, 450), transparent=True, scaling=[75, 75])
            create_image("butter", MAIN_MENU_IMAGES, player['butter'], (900+75, 450), transparent=True, scaling=[75, 75])
            create_image("flour", MAIN_MENU_IMAGES, player['flour'], (800+75, 530), transparent=True, scaling=[75, 75])
            create_image("sugar", MAIN_MENU_IMAGES, player['sugar'], (900+75, 530), transparent=True, scaling=[75, 75])

            # Weapon
            create_text('weapon', MAIN_MENU_TEXT, player['weapon'], "Times New Roman", 48, (0, 0, 0), (540, 240))
            create_image("weapon_sprite", MAIN_MENU_IMAGES, player['weapon_image'], (540, 420), transparent=True, scaling=[300,300])

            # Wave
            create_text('wave', MAIN_MENU_TEXT, "Wave: " + str(wave), "Times New Roman", 60, (200, 0, 0), (540, 120))
            

        # Screen Updates:

        # Renders all buttons onto the game window

        # Manage background colors
        if SCREEN_STATUS == "TUTORIAL":
            WIN.fill((255, 255, 255))
        if SCREEN_STATUS == "MAIN":
            WIN.fill((255, 255, 228))
        elif SCREEN_STATUS == "SHOP":
            WIN.fill((133, 94, 66))
        if SCREEN_STATUS == "FIGHT" or SCREEN_STATUS == "EVENT":
            WIN.fill((21, 71, 52))
        if SCREEN_STATUS == "UPGRADE":
            WIN.fill((124, 0, 200))
        if SCREEN_STATUS == "VICTORY":
            WIN.fill((0, 255, 0))
        if SCREEN_STATUS == "DEATH":
            WIN.fill((0, 0, 0))
        if SCREEN_STATUS == "ENDING":
            WIN.fill((255,215,0))

        # Render all text and images
        for text in TEXT:
            WIN.blit(TEXT[text][0], TEXT[text][1])
        for image in IMAGES:
            WIN.blit(IMAGES[image][0], IMAGES[image][1])
        
        display.update()

main()