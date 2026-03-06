# ---- Python Modules ---- #
import pygame
import os
import math
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
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, InputHandler, MenuHandler):
        self.enabled = False
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.rootDir = rootDir
        self.menuPlayer = Player(screen, pygame.image.load(os.path.join(self.rootDir, 'assets/spritesheet.png')).convert_alpha(), 0.6, self.LG)
        self.clock = clock
        self.tunneler = tunneler
        self.InputHandler = InputHandler
        self.MenuHandler = MenuHandler
        
        self.menuPlayer.x = 0
        self.menuPlayer.y = 659
        self.menuPlayer.x_direction = 1.5
        self.menuPlayer.Facing = "Right"
        self.menuPlayer.isMoving = True
        
        self.menuTunnelA = pygame.Rect(3, 680, 20, 86) # creates a rectangle to be used.
        self.menuTunnelB = pygame.Rect(1452, 680, 20, 86) # creates a rectangle to be used.

        self.titleLabel = TextLabel(445, 120, "TUNNLER - TEMPORAL MELTDOWN", 72, (200, 200, 255), self.screen)
        self.startButton = TextButton(150, 260, "Start Game", 48, (255,255,255), self.screen)
        self.levelButton = TextButton(150, 330, "Play Levels", 48, (255,255,255), self.screen)
        self.settingsButton = TextButton(150, 400, "Settings", 48, (255,255,255), self.screen)
        self.endButton = TextButton(150, 470, "Quit", 48, (255,255,255), self.screen)
        self.footerLabel = TextLabel(1290, 885, "© 2026 Aperture-Inspired Systems", 28, (180,180,180), self.screen)
        
                
    def movingPlayerAnimation(self):  
        self.menuPlayer.movePlayer(None, None, True) # plays the moving animation as we move the player
        self.menuPlayer.draw(True) #draws on the player
        if self.menuPlayer.rectangle.colliderect(self.menuTunnelB): # when the player reaches the end it tunnels through to the other end and loops back. to show a loading effect
            self.menuPlayer.tunnelPlayer(0,659, self.tunneler.tunnelAColour)
            
        pygame.draw.rect(self.screen, self.tunneler.tunnelAColour, self.menuTunnelA) # draws on the rectangle and correct tunnel colour
        pygame.draw.rect(self.screen, self.tunneler.tunnelBColour, self.menuTunnelB) # draws on the rectangle and correct tunnel colour
        
    def enableUi(self):
        self.enabled = True
        
    def disableUi(self):
        self.enabled = False
        
    def drawCurrentMenu(self):
        if self.enabled == True:
            
            # ---- Drawing on Items ---- #
            self.startButton.draw() # Draws on the start Button
            self.endButton.draw() # Draws on the end Button
            self.settingsButton.draw()
            self.levelButton.draw()
            self.footerLabel.draw()
            self.titleLabel.draw()
                           
            self.movingPlayerAnimation()
              
            # ---- Button Functionality ---- # 
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
                self.InputHandler.inputCheck(event)
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
                        
                    if self.settingsButton.isClicked(event.pos):
                        self.MenuHandler.enableMenu("Settings")
                        
                    if self.levelButton.isClicked(event.pos):
                        self.MenuHandler.enableMenu("LevelSelect")

            
                    print(event.pos)