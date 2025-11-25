# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class TextLabel:
    def __init__(self, x, y, text, font_size, color, screen): # Basic Setup of the text labels and variables it needs.
        
        # Requested variables from when creating a new instance of this class.
        self.screen = screen 
        self.text = text 
        self.color = color

        self.font = pygame.font.Font(None, font_size) # Sets the font of the Text
        self.render = self.font.render(self.text, True, self.color) # Renders the text in the colour and font

        self.rectangle = self.render.get_rect() # Gets the coordinates of the render.
        self.rectangle.topleft = (x, y) # Sets the coordinates of the render to specified x and y coordinates.

    def draw(self):
        self.screen.blit(self.render, (self.rectangle.x, self.rectangle.y)) # On call draws on the text.
