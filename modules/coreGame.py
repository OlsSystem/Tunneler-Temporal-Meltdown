# ---- Python Modules ---- #
import pygame
import os
import modules.utils.ImageButton as ImgButton

# ---- Misc Variables ---- #
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---- Initialising Variables ---- # 

class CoreGame:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((800,500))
        self.isRunning = True
        
        pygame.init()
        
        self.startUp()
        
        
    def startUp(self):
                
        startButton = ImgButton.ImageButton(100,200, pygame.image.load(os.path.join(ROOT_DIR, '../assets/Image.png')).convert_alpha(), 0.7, self.screen)
        
        while self.isRunning:
            
            startButton.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                    pygame.quit()