# PyGame Imports and Initialization
import pygame
import pygame.display as display
from pygame import time
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
MAIN_MENU_TEXT = {}
MAIN_MENU_IMAGES = {}

SHOP_MENU_TEXT = {}
SHOP_MENU_IMAGES = {}

FIGHT_MENU_TEXT = {}
FIGHT_MENU_IMAGES = {}
# Work as Random Access storage for battle stages
# This dictionary will contain the enemies in each stage
# It may be altered at the convenience of the specific stage 
TEMP_ENEMIES = {}


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
ENEMYHP_SCALING = 1.2
ENEMYDMG_SCALING = 1.1
dead = False
player = {
    "health": 10, 
    "damage": 1, 
    "defence": 0, 
    "gold": 0, 
    "weapon": None, 
    'seasoned': False, 
    "chicken": False,
    "sprite": "Images/chef-character.png"
}
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
    if name not in screen:
        # Ensures that the coordinates are interpreted based on the center of the image
        screen.setdefault(name, [text_object, (text_coordinates[0] - text_object.get_width()/2, text_coordinates[1] - text_object.get_height()/2)])
    else:
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
    if name not in screen:
        # Ensures that the coordinates are interpreted based on the center of the image
        screen.setdefault(name, [image_object, (image_coordinates[0] - image_object.get_width()/2, image_coordinates[1] - image_object.get_height()/2)])
    else:
        screen[name] = [image_object, image_coordinates]
    


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
    
    print(button_coordinates[0], button_coordinates[1])

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


def shop_menu(items: list):
    """
    Given a list <items> that contains elements in the format [name, path, coords, scale], 
    render each item to the shop menu.
    """

    global SHOP_MENU_TEXT, SHOP_MENU_IMAGES, WIDTH

    for i in range(len(items)):
        create_image(
            items[i][0], # Name 
            SHOP_MENU_IMAGES, # Location (Dictionary)
            items[i][1], # Path
            (items[i][2][0], items[i][2][1]), # Coordinates
            transparent=True, # Transparency
            scaling=[items[i][3][0], items[i][3][1]] # Size
        )

    create_image("shop back", SHOP_MENU_IMAGES, "Images/arrow.png", (120, 570), transparent=True, scaling=[300, 300])
    create_image("table", SHOP_MENU_IMAGES, "Images/shop-table.png", (540, 560), transparent=True, scaling=[650, 650])


def create_enemy(name: str, health: int, damage: int, sprite_path: str):
    return {"name": name, "hp": health, "dmg": damage, "img": sprite_path}


def tutorial_stage():

    global FIGHT_MENU_TEXT, FIGHT_MENU_IMAGES, TEMP_ENEMIES
    global player, wave

    FIGHT_MENU_TEXT = {}
    FIGHT_MENU_IMAGES = {}
    TEMP_ENEMIES = {}

    enemy_object = create_enemy("Dummy", 10, 0, "Images/amogus-ascended.png")
    TEMP_ENEMIES[enemy_object["name"]] = enemy_object 
        




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


def battle(enemy_stats: dict, player: dict, wave: int):
    """
    A function that runs a battle process between the user and an enemy.
    """
    
    global FIGHT_MENU_IMAGES, FIGHT_MENU_TEXT, TEMP_ENEMIES
    global dead


    # Put the user in the battle loop
    in_battle = True
    while in_battle:
        
        # Render all text and images
        WIN.fill((124, 252, 0))
        for text in FIGHT_MENU_TEXT:
            WIN.blit(FIGHT_MENU_TEXT[text][0], FIGHT_MENU_TEXT[text][1])
        for image in FIGHT_MENU_IMAGES:
            WIN.blit(FIGHT_MENU_IMAGES[image][0], FIGHT_MENU_IMAGES[image][1])
        
        # Print the stats of the enemy
        print(f"You are about to fight {enemy_name}!")
        print(f"{enemy_name}'s stats:")
        input()



    """
    time_elapsed = 0
    # Loops through a fight until either party falls below 0 hp.
    while hp > 0 and enemy_hp > 0:
        downtime = clock.tick(30)
        time_elapsed += downtime
        if time_elapsed > 500:
            time_elapsed = 0 
            if player['weapon'] != None:
                damage_c = dmg * player["weapon"]["damage"]
                enemy_hp = round((enemy_hp - damage_c), 2)
            else:
                enemy_hp = round((enemy_hp - dmg), 2)

            hp = round(hp - (enemy_dmg * (1 - (defence/10))), 2)
            if enemy_hp < 0:
                enemy_hp = 0
            if hp < 0:
                hp = 0

            print(f"{enemy_stats['name']}'s Health: {enemy_hp}\n Your Health: {hp}")
        
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
    """


#---------------Game Loop---------------# 


def main():

    global SCREEN_STATUS, wave
    global TEMP_ENEMIES

    # Initialize the game for the first playthrough
    SCREEN_STATUS = "MAIN"
    wave = 0
    # manage_music()

    # Initialize the images and text for each menu
    # via their respective functions
    main_menu()
    shop_menu([
                ["cs", "Images/chopstick.png", (125, 100), [200,200]],
                ["fp", "Images/frying-pan.png", (750, 100), [200,200]],
                ["kf", "Images/knife.png", (485, 100), [300,300]],
                ["sp", "Images/spatula.png", (250, 100), [300, 300]]
            ])
        
    # Important flags and accumulators
    clicks = 0
    running = True


    # Actual Game Loop
    while running:

        # User Interface
        if SCREEN_STATUS == "MAIN":
            TEXT = MAIN_MENU_TEXT
            IMAGES = MAIN_MENU_IMAGES
            
        elif SCREEN_STATUS == "SHOP":
            TEXT = SHOP_MENU_TEXT
            IMAGES = SHOP_MENU_IMAGES

        elif SCREEN_STATUS == "FIGHT":
            TEXT = FIGHT_MENU_TEXT
            IMAGES = FIGHT_MENU_IMAGES
        
        

        # Track the (x, y) coordinates of the mouse
        # relative to the game window
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            # Closing the window ends the game
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                print(mouse_pos)
                current_enemy = ""

                # If FIGHT text or icon is clicked
                if check_button_coords(mouse_pos, MAIN_MENU_TEXT["fight"]) == True or check_button_coords(mouse_pos, MAIN_MENU_IMAGES["fight"]) == True:
                    if SCREEN_STATUS != "FIGHT":
                        SCREEN_STATUS = "FIGHT"
                        # manage_music()
                        if wave == 0:
                            create_image("dummy", FIGHT_MENU_IMAGES, "Images/amogus-ascended.png", (540, 360), transparent=True, scaling=[400, 400])
                            current_enemy = "dummy"

                if SCREEN_STATUS == "FIGHT":
                    if check_button_coords(mouse_pos, FIGHT_MENU_IMAGES["dummy"]) == True:
                        print("You clicked on the fight screen!")

                # If SHOP text or icon is clicked
                elif check_button_coords(mouse_pos, MAIN_MENU_TEXT["shop"]) == True or check_button_coords(mouse_pos, MAIN_MENU_IMAGES["shop"]) == True:
                    if SCREEN_STATUS != "SHOP":
                        SCREEN_STATUS = "SHOP"
                        # manage_music()

                # If SHOP_BACK button is clicked
                elif check_button_coords(mouse_pos, SHOP_MENU_IMAGES["shop back"]) == True:
                    if SCREEN_STATUS != "MAIN":
                        SCREEN_STATUS = "MAIN"
                        # manage_music()


        # Screen Updates:

        # Renders all buttons onto the game window

        # Manage background colors
        if SCREEN_STATUS == "MAIN":
            WIN.fill((255, 255, 228))
        elif SCREEN_STATUS == "SHOP":
            WIN.fill((133, 94, 66))
        if SCREEN_STATUS == "FIGHT":
            WIN.fill((124, 252, 0))
    
        # Render all text and images
        for text in TEXT:
            WIN.blit(TEXT[text][0], TEXT[text][1])
        for image in IMAGES:
            WIN.blit(IMAGES[image][0], IMAGES[image][1])
        
        display.update()

main()