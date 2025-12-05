# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class SpriteSheet:
    def __init__(self, sheet):
        self.spriteSheet = sheet # Initialises the image as the sprite sheet
        
    def getSprite(self, frame, width, height, scale, colour):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha() # creates a surface for the sprite to be on. 
        
        sprite.blit(self.spriteSheet, (0,0), ((frame * width), 0, width, height)) # blit the sprite sheet onto the surface
        sprite = pygame.transform.scale(sprite, (width * scale, height * scale)) # scales the image to the correct dimentions of our character.
        
        sprite.set_colorkey(colour) # keys out the background colour 
        
        return sprite # returns the frame that the has been requested