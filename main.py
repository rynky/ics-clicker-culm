# PyGame Imports and Initialization
import pygame
import pygame.display as display
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

# Works as Random Access storage for battle stages
# This dictionary will contain the enemies in each stage
# It may be altered at the convenience of the specific stage 
TEMP_ENEMIES = {}

UPGRADE_MENU_TEXT = {}
UPGRADE_MENU_IMAGES = {}

VICTORY_MENU_TEXT = {}
VICTORY_MENU_IMAGES = {}


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
in_battle = False
dead = False
enemy_cooldown = 0
last_frame = clock.tick(30)
player = {
    "health": 10, 
    "damage": 1, 
    "defence": 0, 
    "gold": 10, 
    
    # The spoon has a damage of 1
    "weapon": "Spoon",

    # weapon multiplier = 1 + (weapon_damage - 1)/4
    "weapon_multiplier": 1,
    
    'seasoned': False, 
    "chicken": False,
    "sprite": "Images/chef-character.png"
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


#---------------Game Loop---------------# 


def main():

    global SCREEN_STATUS, wave, weapons
    global TEMP_ENEMIES, in_battle, enemy_cooldown
    global clock, last_frame

    weapons = {
        "Chopsticks": {"cost": 5, "damage": 2},
        "Spatula": {"cost": 8, "damage": 3},
        "Knife": {"cost": 10, "damage": 4},
        "Frying Pan": {"cost": 12, "damage": 5}
    }
    
    # Initialize the game for the first playthrough
    SCREEN_STATUS = "MAIN"
    wave = 0
    # manage_music()

    # Initialize the images and text for each menu
    # via their respective functions
    main_menu()
    shop_menu([
                ["cs", "Images/chopstick.png", (200, 320), [225,225]],
                ["sp", "Images/spatula.png", (415, 280), [335, 335]],
                ["kf", "Images/knife.png", (665, 280), [335,335]],
                ["fp", "Images/frying-pan.png", (900, 320), [225,225]]

            ])
    upgrade_menu([
                ["health", "Images/heart.png", (100, 300), [200,200]],
                ["defence", "Images/shield.png", (100, 450), [200,200]],
                ["damage", "Images/sword.png", (100, 600), [200,200]]
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
        
        elif SCREEN_STATUS == "UPGRADE":
            TEXT = UPGRADE_MENU_TEXT
            IMAGES = UPGRADE_MENU_IMAGES

        elif SCREEN_STATUS == "VICTORY":
            TEXT = VICTORY_MENU_TEXT
            IMAGES = VICTORY_MENU_IMAGES
        
        # Track the (x, y) coordinates of the mouse
        # relative to the game window
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            # Closing the window ends the game
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Function for each menu
                if SCREEN_STATUS == "MAIN":
                    if check_button_coords(mouse_pos, MAIN_MENU_TEXT["fight"]) == True or check_button_coords(mouse_pos, MAIN_MENU_IMAGES["fight"]) == True:
                        SCREEN_STATUS = "FIGHT"
                    elif check_button_coords(mouse_pos, MAIN_MENU_TEXT["shop"]) == True or check_button_coords(mouse_pos, MAIN_MENU_IMAGES["shop"]) == True:
                        SCREEN_STATUS = "SHOP"
                    elif check_button_coords(mouse_pos, MAIN_MENU_TEXT["upgrade"]) == True or check_button_coords(mouse_pos, MAIN_MENU_IMAGES["upgrade"]) == True:
                        SCREEN_STATUS = "UPGRADE"


                if SCREEN_STATUS == "FIGHT":

                    print(enemy_cooldown)

                    if wave == 0:
                        
                        if in_battle == False:
                            
                            # Reset the menu images and text
                            FIGHT_MENU_IMAGES = {}
                            FIGHT_MENU_TEXT = {}

                            # Render the enemy sprite
                            create_image("dummy", FIGHT_MENU_IMAGES, "Images/amogus-ascended.png", (540, 360), transparent=True, scaling=[400, 400])
                            create_enemy("dummy", 10, 1)

                            # Create temporary variables for the battle
                            player_hp = player["health"]

                            enemy_hp = TEMP_ENEMIES["dummy"]["hp"]
                            enemy_dmg = TEMP_ENEMIES["dummy"]["dmg"]

                            # Render the enemy and player health stats
                            create_text("enemy health", FIGHT_MENU_TEXT, f"Enemy Health: {enemy_hp}", "Times New Roman", 64, (255, 0, 0), (540, 50))

                            create_image("player health", FIGHT_MENU_IMAGES, "Images/heart.png", (780, 680), transparent=True, scaling=[75,75])
                            create_text("player health", FIGHT_MENU_TEXT, f"Health: {player_hp}", "Times New Roman", 48, (0, 0, 0), (920, 675))
                            
                            # Begin the Battle Loop
                            in_battle = True
                            enemy_cooldown = 0
                            print(f"Enemy Health: {enemy_hp}")
                        
                        else:

                            # Increment the cooldown with respect
                            # to the frame rate of the game (30 FPS)
                            enemy_cooldown += last_frame

                            # If the cooldown has reached <arbitrary value>, 
                            # deal damage to the player
                            if enemy_cooldown > 300: 
                                enemy_cooldown = 0
                                player_hp -= enemy_dmg
                            
                            # Check if the enemy has been clicked
                            if check_button_coords(mouse_pos, FIGHT_MENU_IMAGES["dummy"]) == True:
                                
                                # Damage calculations
                                player_damage = player['damage'] * player['weapon_multiplier']
                                enemy_hp -= player_damage

                                print(f"\nYou did {player_damage} damage!")
                                print(f"Enemy Health: {enemy_hp}")

                                # Ends the battle when the enemy or player health is 0
                                if enemy_hp <= 0 or player_hp <= 0:

                                    # Reset the Victory and Loss menus
                                    VICTORY_MENU_TEXT = {}
                                    VICTORY_MENU_IMAGES = {}
                                    
                                    # Handles win and loss cases
                                    if enemy_hp <= 0:
                                        print("VICTORY")
                                        enemy_hp = 0
                                        
                                        create_text("dummy", VICTORY_MENU_TEXT, f'YOU HAVE SLAIN DUMMY', "Times New Roman", 48, (0, 0, 0), (540, 300))
                                        create_text("continue", VICTORY_MENU_TEXT, f'>> Click Here to Continue <<', "Times New Roman", 48, (255, 0, 0), (540, 400))

                                        SCREEN_STATUS = "VICTORY"

                                    elif player_hp <= 0:
                                        player_hp = 0

                                    # End the battle process
                                    in_battle = False
                                    wave += 1

                            # Update the enemy and player health text
                            create_text("player health", FIGHT_MENU_TEXT, f"Health: {player_hp}", "Times New Roman", 48, (0, 0, 0), (920, 675))
                            create_text("enemy health", FIGHT_MENU_TEXT, f"Enemy Health: {enemy_hp}", "Times New Roman", 64, (255, 0, 0), (540, 50))


                    elif wave % 5 == 0:
                        print("Boss")

                    elif wave % 10 == 3 or wave % 10 == 8:
                        print("Random Event")

                
                elif SCREEN_STATUS == "VICTORY":
                    
                    # If you are on the victory screen,
                    # allow the continue button to switch to
                    # the main menu
                    if check_button_coords(mouse_pos, VICTORY_MENU_TEXT["continue"]):
                        SCREEN_STATUS = "MAIN"


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
                            player['gold'] -= weapons[shop_choice]["cost"]
                            player["weapon_multiplier"] = 1 + (weapons[shop_choice]["damage"] - 1)/4
                            weapons[shop_choice]["cost"] = "SOLD :("
                            create_text("buy_note", SHOP_MENU_TEXT, "You successfully bought: " + shop_choice, "Times New Roman", 36, (0, 0, 0), (540, 75))
      

                elif SCREEN_STATUS == "UPGRADE":
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


            create_text("gold_count", MAIN_MENU_TEXT, str(player['gold']), "Times New Roman", 48, (0, 0, 0), (975, 75))
            create_text("gold_count", UPGRADE_MENU_TEXT, str(player['gold']), "Times New Roman", 48, (0, 0, 0), (975, 75))
            create_text("gold_count", SHOP_MENU_TEXT, str(player['gold']), "Times New Roman", 48, (0, 0, 0), (975, 75)) 


            

        # Screen Updates:

        # Renders all buttons onto the game window

        # Manage background colors
        if SCREEN_STATUS == "MAIN":
            WIN.fill((255, 255, 228))
        elif SCREEN_STATUS == "SHOP":
            WIN.fill((133, 94, 66))
        if SCREEN_STATUS == "FIGHT":
            WIN.fill((124, 252, 0))
        if SCREEN_STATUS == "UPGRADE":
            WIN.fill((124, 0, 200))
        if SCREEN_STATUS == "VICTORY":
            WIN.fill((255, 255, 255))

        # Render all text and images
        for text in TEXT:
            WIN.blit(TEXT[text][0], TEXT[text][1])
        for image in IMAGES:
            WIN.blit(IMAGES[image][0], IMAGES[image][1])
        
        display.update()

main()