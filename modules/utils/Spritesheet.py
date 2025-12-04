# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class SpriteSheet:
    def __init__(self, sheet):
        self.spriteSheet = sheet
        
    def getSprite(self, frame, width, height, scale, colour):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        
        sprite.blit(self.spriteSheet, (0,0), ((frame * width), 0, width, height))
        sprite = pygame.transform.scale(sprite, (width * scale, height * scale))
        
        sprite.set_colorkey(colour)
        
        return sprite