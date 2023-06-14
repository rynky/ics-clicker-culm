import pygame
import pygame.display as display
window = display.set_mode((1280,720))
display.set_caption("ICS3U - Raiyan and Raymond")
display.flip()

"""
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

EVENT_MENU_TEXT = {}
EVENT_MENU_IMAGES = {}

UPGRADE_MENU_TEXT = {}
UPGRADE_MENU_IMAGES = {}

VICTORY_MENU_TEXT = {}
VICTORY_MENU_IMAGES = {}

DEAD_MENU_TEXT = {}
DEAD_MENU_IMAGES = {}


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
BOSS_MOVEMENT_FACTOR = 0.95

in_battle = False
in_boss_battle = False
dead = False
enemy_cooldown = 0
last_frame = clock.tick(1)
last_enemy = ""

in_event = False
completed_events = []

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
    
    number = 1
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

    global SCREEN_STATUS, TEMP_ENEMIES
    global player, wave, weapons, last_enemy
    global in_battle, in_event, in_boss_battle
    global clock, last_frame, enemy_cooldown
    
    EVENT_MENU_TEXT = {}
    EVENT_MENU_IMAGES = {}
    
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
                        ending = None
                        event_number = random_event()
                        print("This code is running", event_number)
                        in_event = True

                    # Butcher event
                    if in_event == True:
                        
                        if event_number == 1:

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
                                if check_button_coords(mouse_pos, EVENT_MENU_TEXT["yes"]) == True:
                                    ending = 1
                                    ending_screen = True
                                    first_screen = False
                                elif check_button_coords(mouse_pos, EVENT_MENU_TEXT["no"]) == True:
                                    EVENT_MENU_TEXT = {}
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "How... Unfortunate.", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "I have another offer though.", "Times New Roman", 48, (255, 0, 0), (250+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "Can I buy your arm for 15 gold?", "Times New Roman", 48, (255, 0, 0), (250+100, 456-100))
                                    create_text("yes", EVENT_MENU_TEXT, "[Yes]", "Times New Roman", 48, (255, 0, 0), (100, 456-100+96))
                                    create_text("no", EVENT_MENU_TEXT, "[No]", "Times New Roman", 48, (255, 0, 0), (600, 456-100+96))  
                                    second_screen = True
                                    first_screen = False
                                    
                            if second_screen == True:
                                if check_button_coords(mouse_pos, EVENT_MENU_TEXT["yes"]) == True:
                                    ending = 2
                                    second_screen = False
                                    ending_screen = True
                                
                                elif check_button_coords(mouse_pos, EVENT_MENU_TEXT["no"]) == True:
                                    ending = 3
                                    second_screen = False
                                    ending_screen = True

                                
                            if ending_screen == True:
                                EVENT_MENU_TEXT = {}
                                if ending == 1:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "Thanks! You can start now!", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "He pays you, and you get stronger.", "Times New Roman", 48, (255, 0, 0), (250+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "+2 Gold, +1 Damage", "Times New Roman", 48, (255, 0, 0), (250+100, 456-100))
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (250+100, 100))
                                elif ending == 2:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "Great!", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))
                                    create_text("dialogue 2", EVENT_MENU_TEXT, "I've always wanted to try human meat.", "Times New Roman", 48, (255, 0, 0), (250+100, 408-100))
                                    create_text("dialogue 3", EVENT_MENU_TEXT, "+15 Gold, health and damage halved.", "Times New Roman", 48, (255, 0, 0), (250+100, 456-100))
                                    create_image("arm", EVENT_MENU_IMAGES, "Images/arm.png", (400, 560), transparent=True, scaling=[400, 400])
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (250+100, 100))
                                    # UPDATE STATS HERE
                                    # UPDATE CHEF CHARACTER TO ARMLESS SPRITE HERE
                                elif ending == 3:
                                    create_text("dialogue 1", EVENT_MENU_TEXT, "Alright, I'll cya next time.", "Times New Roman", 48, (255, 0, 0), (250+100, 360-100))      
                                    create_text("continue", EVENT_MENU_TEXT, ">>> Click here to continue <<<", "Times New Roman", 48, (255, 0, 0), (250+100, 100))
                                    
                                if check_button_coords(mouse_pos, EVENT_MENU_TEXT["continue"]) == True:
                                    SCREEN_STATUS = "MAIN"
                                    EVENT_MENU_IMAGES = {}
                                    EVENT_MENU_TEXT = {}
                                    wave += 1


            # Mouse clicked
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
                        enemy_name = "Dummy"
                        enemy_sprite = "Images/training_dummy.png"
                        enemy_sprite_size = [400, 400] 
                        create_enemy(enemy_name, 10, 1)
                    
                    elif wave % 5 == 0:

                        if wave == 5:
                            enemy_name = "Burger King"
                            enemy_sprite = "Images/burger_king.png"
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
                                                
                                        create_text("slain", VICTORY_MENU_TEXT, f'YOU HAVE SLAIN {enemy_name.upper()}', "Times New Roman", 48, (0, 0, 0), (540, 300))
                                        create_text("continue", VICTORY_MENU_TEXT, f'>> Click Here to Continue <<', "Times New Roman", 48, (255, 0, 0), (540, 400))

                                        SCREEN_STATUS = "VICTORY"

                                        # End the battle process
                                        in_battle = False
                                        wave += 1
                                        last_enemy = enemy_name
                                        
                                        # End the boss battle, if applicable
                                        if in_boss_battle == True:
                                            in_boss_battle = False


                            # Update the enemy and player health text
                            # Floor and round each value to avoid floating point errors
                            create_text("player health", FIGHT_MENU_TEXT, f"Health: {round(player_hp)}", "Times New Roman", 48, (0, 0, 0), (950, 675))
                            create_text("enemy health", FIGHT_MENU_TEXT, f"Health: {round(enemy_hp)}", "Times New Roman", 64, (255, 0, 0), (540, 50))


                elif SCREEN_STATUS == "VICTORY":
                    
                    # If you are on the victory screen,
                    # allow the continue button to switch to
                    # the main menu
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
                        "gold": 10, 

                        # The spoon has a damage of 1
                        "weapon": "Spoon",

                        # weapon multiplier = 1 + (weapon_damage - 1)/4
                        "weapon_multiplier": 1,

                        'seasoned': False, 
                        "chicken": False,
                        "sprite": "Images/chef-character.png"
                        }
                    
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
        if SCREEN_STATUS == "FIGHT" or SCREEN_STATUS == "EVENT":
            WIN.fill((124, 252, 0))
        if SCREEN_STATUS == "UPGRADE":
            WIN.fill((124, 0, 200))
        if SCREEN_STATUS == "VICTORY":
            WIN.fill((255, 255, 255))
        if SCREEN_STATUS == "DEATH":
            WIN.fill((0, 0, 0))

        # Render all text and images
        for text in TEXT:
            WIN.blit(TEXT[text][0], TEXT[text][1])
        for image in IMAGES:
            WIN.blit(IMAGES[image][0], IMAGES[image][1])
        
        display.update()

main()