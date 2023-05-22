# PyGame Imports and Initialization
import pygame
import pygame.display as display
pygame.init()


#------------Window settings------------# 

WIN = display.set_mode((1280, 720))  # Window Size
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

# Set the font size and type for buttons
BUTTON_FONT_SIZE = 36
BUTTON_FONT = pygame.font.SysFont(None, BUTTON_FONT_SIZE)

# PROTOTYPE CODE
EXIT_BUTTON_TEXT = "Quit Game"  # Store the text
EXIT_BUTTON = BUTTON_FONT.render(EXIT_BUTTON_TEXT, True, (255, 255, 255))  # Render the text
EXIT_BUTTON_WIDTH = EXIT_BUTTON.get_width()  # Get the width of the text
EXIT_BUTTON_HEIGHT = EXIT_BUTTON.get_width()  # Get the height of the text
EXIT_BUTTON_COORDS = ((WIDTH - EXIT_BUTTON_WIDTH)/2, HEIGHT/2)  # Position at the middle of the window


#---------------Functions---------------# 

def check_coords(coordinates: (int, int)) -> bool:
    """
    PROTOTYPE VERSION OF THE FUNCTION.
    This function checks whether the given coordinates, 
    <coordinates>, is inside of the exit button.
    """
    global WIDTH, HEIGHT, EXIT_BUTTON_WIDTH, EXIT_BUTTON_HEIGHT, i
    
    # Checks if the x-coordinates match
    if (WIDTH - EXIT_BUTTON_WIDTH)/2 <= coordinates[0] <= (WIDTH - EXIT_BUTTON_WIDTH)/2 + EXIT_BUTTON_WIDTH:
        # Checks if the y-coordinates match
        if HEIGHT/2 <= coordinates[1] <= (HEIGHT + EXIT_BUTTON_HEIGHT)/2:
            return True  
    return False


#---------------Game Loop---------------# 

running = True
while running:
    
    for event in pygame.event.get():

        # Closing the window ends the game
        if event.type == pygame.QUIT:
            running = False
        
        # Exit game if the exit button is clicked - PROTOTYPE CODE
        if event.type == pygame.MOUSEBUTTONDOWN:
            if check_coords(mouse_pos):
                running = False
    
    # Track the (x, y) coordinates of the mouse
    # relative to the game window
    mouse_pos = pygame.mouse.get_pos()

    # Screen Updates:

    # Renders the exit button onto the game window - PROOTYPE CODE
    WIN.blit(EXIT_BUTTON, EXIT_BUTTON_COORDS)
    
    display.update()
