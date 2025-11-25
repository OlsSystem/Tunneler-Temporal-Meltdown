# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Cursor:
    def __init__(self, x, y, image, scale, screen):
      
      # Requested variables from when creating a new instance of this class.
      self.width = image.get_width()
      self.height = image.get_height()
      self.screen = screen
      
      self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale))) # Scales down the image using the scale requested
      self.rectangle = self.image.get_rect() # Gets the coordinates of the render.
      self.rectangle.topleft = (x,y) # Sets the coordinates of the render to specified x and y coordinates.

    def draw(self):
        self.screen.blit(self.image, (self.rectangle.x, self.rectangle.y)) # Draws on the cursor at the requested coordinates
        
    def moveCursor(self, x, y):
        self.rectangle.topleft = (x,y) # Sets the new coordinates of the hand to the cursor
        self.screen.blit(self.image, (self.rectangle.x, self.rectangle.y)) # Draws on the cursor at the requested coordinates
