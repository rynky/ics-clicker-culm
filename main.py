# PyGame Imports and Initialization
import pygame
import pygame.display as display
pygame.init()

"""
For this project, the <BUTTONS> dictionary will contain all the buttons and their icons.
Each button entry will be stored as such:

BUTTON_NAME : [BUTTON_OBJECT, BUTTON_COORDINATES]

Similarly, all images will be stored in various image dictionaries, for each screen.

IMAGE_NAME : [IMAGE_OBJECT, IMAGE_COORDINATES]
"""
MAIN_MENU_TEXT = {}
MAIN_MENU_IMAGES = {}

SHOP_MENU_TEXT = {}
SHOP_MENU_IMAGES = {}


#------------Window settings------------# 

WIN = display.set_mode((1080, 720))  # Window Size
HEIGHT = WIN.get_height()
WIDTH = WIN.get_width()
display.set_caption("Medieval Munchies")
display.flip()  # Screen Update
SCREEN_STATUS = "MAIN"  # Track which screen the user is on


#-------------Text settings-------------# 

""" 
RGB Values:
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
"""

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
        screen.setdefault(name, [text_object, text_coordinates])
    else:
        screen[name] = [text_object, text_coordinates]
    

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
        screen.setdefault(name, [image_object, image_coordinates])
    else:
        screen[name] = [image_object, image_coordinates]
    


def check_button_coords(coordinates: (int, int), button: pygame.font, button_coordinates: (int, int)) -> bool:
    """
    This function checks whether the given coordinates, <coordinates>, are inside of a button.
    """
    global WIDTH, HEIGHT 
    
    BUTTON_WIDTH = button.get_width()
    BUTTON_HEIGHT = button.get_height()
    
    # Checks if the x-coordinates match
    if button_coordinates[0] <= coordinates[0] <= button_coordinates[0] + BUTTON_WIDTH:
        
        # Checks if the y-coordinates match
        if button_coordinates[1] <= coordinates[1] <= button_coordinates[1] + BUTTON_HEIGHT:
            return True  
    
    return False


def main_menu():
    """
    Display the main menu in its entirety with all its text and images.
    """

    create_text("title", MAIN_MENU_TEXT, "Medieval Munchies", "Times New Roman", 64, (0, 0, 0), (300, 0))

    create_image("player", MAIN_MENU_IMAGES, "Images/chef-character.png", (-75, 45), transparent=True, scaling=[600, 600])

    create_text("upgrade", MAIN_MENU_TEXT, "UPGRADE", "Times New Roman", 48, (219, 172, 52), ((WIDTH - 984)/2, HEIGHT/2 + 225))
    create_image("upgrade", MAIN_MENU_IMAGES, "Images/anvil.png", (WIDTH - 800, HEIGHT/2 + 200), transparent=True, scaling=[120, 120])
    
    create_text("fight", MAIN_MENU_TEXT, "FIGHT", "Times New Roman", 48, (255, 0, 0), ((WIDTH - 158)/2, HEIGHT/2 + 225))
    create_image("fight", MAIN_MENU_IMAGES, "Images/carrot-sword.png", (WIDTH/2 + 65, HEIGHT/2 + 212.5), transparent=True, scaling=[80, 80])

    create_text("shop", MAIN_MENU_TEXT, "SHOP", "Times New Roman", 48, (17, 140, 79), (WIDTH - 325, HEIGHT/2 + 225))
    create_image("shop", MAIN_MENU_IMAGES, "Images/shopping-cart.png", (WIDTH - 180, HEIGHT/2 + 212.5), transparent=True, scaling=[80, 80])


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


#---------------Game Loop---------------# 


def main():

    global SCREEN_STATUS
    SCREEN_STATUS = "SHOP"
        
    # Important flags and accumulators
    clicks = 0
    running = True

    # User Interface
    if SCREEN_STATUS == "MAIN":
        TEXT, IMAGES = MAIN_MENU_IMAGES, MAIN_MENU_TEXT
        main_menu()
    elif SCREEN_STATUS == "SHOP":
        TEXT, IMAGES = SHOP_MENU_IMAGES, SHOP_MENU_TEXT
        shop_menu([
            ["cs", "Images/chopstick.png", (125, 16), [200,200]],
            ["fp", "Images/frying-pan.png", (750, 27), [200,200]],
            ["kf", "Images/knife.png", (485, 0), [300,300]],
            ["sp", "Images/spatula.png", (250, 0), [300, 300]]
        ])

    # Actual Game Loop
    while running:

        for event in pygame.event.get():

            # Closing the window ends the game
            if event.type == pygame.QUIT:
                running = False
        
        # Track the (x, y) coordinates of the mouse
        # relative to the game window
        mouse_pos = pygame.mouse.get_pos()

        # Screen Updates:

        # Renders all buttons onto the game window
        WIN.fill((255, 255, 228))  # Fill the screen with the background color before rendering
        for text in TEXT:
            WIN.blit(TEXT[text][0], TEXT[text][1])
        for image in IMAGES:
            WIN.blit(IMAGES[image][0], IMAGES[image][1])
        
        display.update()

main()