# PyGame Imports and Initialization
import pygame
import pygame.display as display
pygame.init()

"""
For this project, the <BUTTONS> dictionary will contain all the buttons and their properties.
Each button entry will be stored as such:

BUTTON_NAME : [BUTTON_OBJECT, BUTTON_COORDINATES]
"""
BUTTONS = {}

#------------Window settings------------# 

WIN = display.set_mode((1080, 720))  # Window Size
HEIGHT = WIN.get_height()
WIDTH = WIN.get_width()
display.set_caption("ICS3U - Raiyan and Raymond")
display.flip()  # Screen Update


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

def create_button(name: str, 
                  text: str, 
                  font_name: str, 
                  font_size: int, 
                  color: (int, int, int), 
                  button_coordinates: (int, int), 
                  anti_aliasing = True):
    """
    Given all the parameters required to initialize a button, render a <pygame.font> object.
    Additionally, forward the object and its coordinates to the global dictionary <BUTTONS>, 
    which stores all the buttons on the game window.
    The <anti-alasing> parameter determines the smoothness of the font, so it is defaulted to True
    for maximum smoothing.
    """
    global BUTTONS

    button_object = pygame.font.SysFont(font_name, font_size).render(text, anti_aliasing, color)
    if name not in BUTTONS:
        BUTTONS.setdefault(name, [button_object, button_coordinates])
    else:
        BUTTONS[name] = [button_object, button_coordinates]


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


#---------------Game Loop---------------# 

# Important flags and accumulators
clicks = 0
running = True

# Create buttons
create_button("main", "Click Me!", None, 96, (255, 255, 255), ((WIDTH - 158)/2, HEIGHT/2))  # Main button
create_button("counter", f"Clicks: {clicks}", None, 48, (0, 255, 0), (5, 5))  # Counter
create_button("upgrade", "UPGRADE", None, 48, (255, 255, 0), ((WIDTH - 984)/2, (HEIGHT+400)/2))
create_button("fight", "FIGHT", None, 48, (255, 255, 0), ((WIDTH - 108)/2, (HEIGHT+400)/2))
create_button("shop", "SHOP", None, 48, (255, 255, 0), (WIDTH-196, (HEIGHT+400)/2))

# Actual Game Loop
while running:

    for event in pygame.event.get():

        # Closing the window ends the game
        if event.type == pygame.QUIT:
            running = False
        
        # Increment counter if the main button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if check_button_coords(mouse_pos, BUTTONS["main"][0], BUTTONS["main"][1]):
                
                clicks += 1

                # Re-render the counter button
                create_button("counter", f"Clicks: {clicks}", None, 48, (0, 255, 0), (5, 5))  # Counter
                
    
    # Track the (x, y) coordinates of the mouse
    # relative to the game window
    mouse_pos = pygame.mouse.get_pos()

    # Screen Updates:

    # Renders all buttons onto the game window
    WIN.fill((0, 0, 0))  # Fill the screen with the background color before rendering
    for button in BUTTONS:
        WIN.blit(BUTTONS[button][0], BUTTONS[button][1])
    
    display.update()
