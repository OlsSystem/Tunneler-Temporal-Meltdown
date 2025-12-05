# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Cursor():
    def __init__(self, x, y, idleHand, selectHand, scale, screen):
      # Requested variables from when creating a new instance of this class.
      self.selectHand = selectHand
      self.handMode = "Idle"
      self.idleHand = idleHand
      self.hand = self.idleHand
      self.scale = scale
      self.width = self.hand.get_width()
      self.height = self.hand.get_height()
      self.screen = screen
      
      self.image = pygame.transform.scale(self.hand, (int(self.width * scale), int(self.height * scale))) # Scales down the image using the scale requested
      self.rectangle = self.image.get_rect() # Gets the coordinates of the render.
      self.rectangle.topleft = (x,y) # Sets the coordinates of the render to specified x and y coordinates.

    def setImage(self, imageName):
      if imageName == "Select":
        self.hand = self.selectHand # Change the hand to the select image
        self.width = self.hand.get_width()
        self.height = self.hand.get_height()
        self.handMode = "Select" # Set the new Hand Mode
        
        self.image = pygame.transform.scale(self.hand, (int(self.width * 0.6), int(self.height * 0.6))) # Scales down the image using the scale requested
      else:
        self.hand = self.idleHand
        self.handMode = "Idle"
        self.width = self.hand.get_width()
        self.height = self.hand.get_height()
        
        self.image = pygame.transform.scale(self.hand, (int(self.width * self.scale), int(self.height * self.scale))) # Scales down the image using the scale requested
        
      self.draw() # Draw on the new hand.

    def draw(self):
        self.screen.blit(self.image, (self.rectangle.x, self.rectangle.y)) # Draws on the cursor at the requested coordinates
        
    def moveCursor(self, x, y):
        self.rectangle.topleft = (x,y) # Sets the new coordinates of the hand to the cursor
        self.screen.blit(self.image, (self.rectangle.x, self.rectangle.y)) # Draws on the cursor at the requested coordinates
