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


class LoadingScreen():
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, inputHandler, menuHandler):
        self.enabled = False
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.rootDir = rootDir
        self.menuPlayer = Player(screen, pygame.image.load(os.path.join(self.rootDir, 'assets/spritesheet.png')).convert_alpha(), 0.6, self.LG)
        self.clock = clock
        self.tunneler = tunneler
        self.InputHandler = inputHandler
        self.MenuHandler = menuHandler

        self.menuPlayer.x = 0
        self.menuPlayer.y = 659
        self.menuPlayer.x_direction = 1.5
        self.menuPlayer.Facing = "Right"
        self.menuPlayer.isMoving = True
        
        self.menuTunnelA = pygame.Rect(3, 680, 20, 86) # creates a rectangle to be used.
        self.menuTunnelB = pygame.Rect(1452, 680, 20, 86) # creates a rectangle to be used.

        self.testLabel = TextLabel(736, 448, "Loading Level", 60, (255,0,255), self.screen) # Creates a new Label    
        
    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False
        
    def movingPlayerAnimation(self):  
        self.menuPlayer.movePlayer(None) # plays the moving animation as we move the player
        self.menuPlayer.draw(True) #draws on the player
        if self.menuPlayer.rectangle.colliderect(self.menuTunnelB): # when the player reaches the end it tunnels through to the other end and loops back. to show a loading effect
            self.menuPlayer.tunnelPlayer(0,659, self.tunneler.tunnelAColour)
            
        pygame.draw.rect(self.screen, self.tunneler.tunnelAColour, self.menuTunnelA) # draws on the rectangle and correct tunnel colour
        pygame.draw.rect(self.screen, self.tunneler.tunnelBColour, self.menuTunnelB) # draws on the rectangle and correct tunnel colour

    def drawCurrentMenu(self):
        if self.enabled == True:
            self.testLabel.draw() # Draw on the text
                        
            self.movingPlayerAnimation() # runs animation
            
            for event in pygame.event.get(): # Constantly Event Checking.    
                self.InputHandler.inputCheck(event)