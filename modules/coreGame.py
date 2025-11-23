# ---- Python Modules ---- #
import pygame
import os
import modules.utils.ImageButton as ImgButton
from modules.utils.TextButton import TextButton
from modules.handTracking import TrackHands
# ---- Misc Variables ---- #

# ---- Initialising Variables ---- # 

class CoreGame:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((800,500))
        self.isRunning = True
        self.HT = TrackHands()
                
        self.startUp()
        
        
    def startUp(self):
        
        startButton = TextButton(100, 300, "Start", 38, (255,255,255), self.screen)
        endButton = TextButton(100, 100, "End", 38, (255,255,255), self.screen)

        
        while self.isRunning:
            self.screen.fill((30,30,30))
            startButton.draw()
            endButton.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                    pygame.quit()
                    self.HT.stop()
                    break
                    
                if startButton.isClicked(event):
                    print('CLICKED START')
                    self.HT.start()
                    
                if endButton.isClicked(event):
                    print('CLICKED END')
                    self.HT.stop()
                    
                    
            pygame.display.update()