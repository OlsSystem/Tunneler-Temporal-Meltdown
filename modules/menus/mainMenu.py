# ---- Python Modules ---- #
import pygame
import os
from threading import Thread
from modules.utils.ImageButton import ImageButton
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.Player import Player

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)

# ---- Initialising Variables ---- # 


class MainMenu():
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler):
        self.enabled = False
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.rootDir = rootDir
        self.menuPlayer = Player(screen, pygame.image.load(os.path.join(self.rootDir, 'assets/spritesheet.png')).convert_alpha(), 0.6)
        self.clock = clock
        self.tunneler = tunneler

        self.menuPlayer.x = 0
        self.menuPlayer.y = 659
        self.menuPlayer.x_direction = 1.5
        self.menuPlayer.Facing = "Right"
        self.menuPlayer.isMoving = True
        
        self.menuTunnelA = pygame.Rect(3, 680, 20, 86) # creates a rectangle to be used.
        self.menuTunnelB = pygame.Rect(1452, 680, 20, 86) # creates a rectangle to be used.


        self.startButton = TextButton(100, 300, "Start", 38, (255,255,255), self.screen) # Creates a new Start button
        self.endButton = TextButton(100, 380, "End", 38, (255,255,255), self.screen) # Creates a new End button

        self.testLevelLoad1 = TextButton(300, 100, "Test Level 1", 38, (255,209, 21), self.screen) 
        self.testLevelLoad2 = TextButton(300, 200, "Test Level 2", 38, (255,209, 21), self.screen)

        self.testLabel = TextLabel(210, 200, "This is a Test Label", 60, (255,0,255), self.screen) # Creates a new Label    
        
        
    def enableUi(self):
        self.enabled = True
        
    def disableUi(self):
        self.enabled = False
        
    def movingPlayerAnimation(self):
        
        self.menuPlayer.movePlayer(None)
        self.menuPlayer.draw()
        if self.menuPlayer.rectangle.colliderect(self.menuTunnelB):
            self.menuPlayer.tunnelPlayer(0,659, self.tunneler.tunnelAColour)
        pygame.draw.rect(self.screen, self.tunneler.tunnelAColour, self.menuTunnelA) # draws on the rectangle and correct tunnel colour
        pygame.draw.rect(self.screen, self.tunneler.tunnelBColour, self.menuTunnelB) # draws on the rectangle and correct tunnel colour

    def drawCurrentMenu(self):
        if self.enabled == True:
            
            self.startButton.draw() # Draws on the start Button
            self.testLevelLoad1.draw()
            self.testLevelLoad2.draw()
            self.endButton.draw() # Draws on the end Button
            self.testLabel.draw() # Draw on the text
                        
            self.movingPlayerAnimation()
            
            if self.HT.menuTracked and self.cursor.handMode == "Select":
                if self.endButton.isClicked(self.cursor.rectangle.topleft):
                    print('CLICKED END')
                    self.HT.stop() # Closes out the Hand Tracking Client
                    self.HT.disableMenuTracking() # Disabes the menu hand tracking.
                    self.LG.levelEnded()
            
                if self.testLevelLoad2.isClicked(self.cursor.rectangle.topleft):
                    print('CLICKED TEST LOAD 2')
                    self.LG.loadLevel("CH1", "LV2")
            
                if self.testLevelLoad1.isClicked(self.cursor.rectangle.topleft):
                    print('CLICKED TEST LOAD 1')
                    self.LG.loadLevel("CH1", "LV1")
                
            for event in pygame.event.get(): # Constantly Event Checking.    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # When the event is mouse button and down and event button is 1 (keydown)
                    if self.startButton.isClicked(event.pos): # When the start Buttons clicked 
                        print('CLICKED START')
                        self.HT.start() # Opens up the Hand Tracking Client
                        self.HT.enableMenuTracking(self.cursor) # Enables the menu hand tracking.
                    
                    if self.endButton.isClicked(event.pos): # When the end Button clicked
                        print('CLICKED END')
                        self.HT.stop() # Closes out the Hand Tracking Client
                        self.HT.disableMenuTracking() # Disabes the menu hand tracking.
                        self.LG.levelEnded()
            
                    print(event.pos)