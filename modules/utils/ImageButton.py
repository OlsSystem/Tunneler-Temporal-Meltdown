# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class ImageButton:
    def __init__(self, x, y, image, scale, screen):
      self.width = image.get_width()
      self.height = image.get_width()
      self.screen = screen
      
      self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
      self.rectangle = self.image.get_rect()
      self.rectangle.topleft = (x,y)
      
    
    def draw(self):
        self.screen.blit(self.image, (self.rectangle.x, self.rectangle.y))