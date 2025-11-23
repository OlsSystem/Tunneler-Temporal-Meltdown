# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 

class TextButton:
    def __init__(self, x, y, text, font_size, color, screen):
        self.screen = screen
        self.text = text
        self.color = color

        self.font = pygame.font.Font(None, font_size) 
        self.render = self.font.render(self.text, True, self.color)

        self.rectangle = self.render.get_rect()
        self.rectangle.topleft = (x, y)

    def draw(self):
        self.screen.blit(self.render, (self.rectangle.x, self.rectangle.y))
        
    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rectangle.collidepoint(event.pos):
                return True
            else: 
                return False