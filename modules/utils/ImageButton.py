# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class ImageButton():
    def __init__(self, x, y, image, scale, screen):
      
      # Requested variables from when creating a new instance of this class.
      self.width = image.get_width()
      self.height = image.get_height()
      self.screen = screen
      
      self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale))) # Scales down the image using the scale requested
      self.rectangle = self.image.get_rect() # Gets the coordinates of the render.
      self.rectangle.topleft = (x,y) # Sets the coordinates of the render to specified x and y coordinates.

    def draw(self):
        self.screen.blit(self.image, (self.rectangle.x, self.rectangle.y)) # Draws on the image at the requested coordinates
        
    def isClicked(self, pos):
        if self.rectangle.collidepoint(pos): # Checks that where the mouse is and if its on top of the button it returns true
            return True
        else: 
            return False