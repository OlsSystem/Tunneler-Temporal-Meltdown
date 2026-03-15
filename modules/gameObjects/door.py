# ---- Python Modules ---- #
import pygame
import os
from modules.utils.ItemMapping import itemImageMap

# ---- Misc Variables ---- #

assetSize = 64

# ---- Initialising Variables ---- # 


class Door():
    def __init__(self, x, y, linkedButton, screen, rootdir, multiButton):
        # maybe have the door be 2 assets so it doesnt just appear to "disapear"
        self.rootDir = rootdir
        self.screen = screen
        self.doorAsset = pygame.image.load(os.path.normpath(os.path.join(self.rootDir, f'../{itemImageMap["Door"]}'))).convert_alpha() # loads the image ready to be used
        self.doorRect = pygame.Rect(x * assetSize, y * assetSize - 1, assetSize, assetSize)
        
        self.x = x
        self.y = y
        
        self.linkedButton = linkedButton    
        self.multiButton = multiButton        
                
    def draw(self):
        # checking if requires multiple inputs
        if self.multiButton:
            allPressed = True
            for button in self.linkedButton: # loop through all the buttons linked to the door
                if not button.beenPressed(): # if one is not pressed sets all to false
                    allPressed = False
            
            if not allPressed: # only prints if all pressed stays true
                self.screen.blit(self.doorAsset, (self.x * assetSize, self.y * assetSize)) # draws assets
        else:
            if not self.linkedButton.beenPressed():
                self.screen.blit(self.doorAsset, (self.x * assetSize, self.y * assetSize)) # draws assets
