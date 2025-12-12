# ---- Python Modules ---- #
#import cv2
import time
import pygame
import os

# ---- Custom Modules ---- #
from modules.handTracking import TrackHands
from modules.utils.ImageButton import ImageButton
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.utils.Cursor import Cursor
from modules.LevelGen import LevelGenerator
from modules.Player import Player
from modules.Items.Tunneler import Tunneler
from modules.utils.Particles import RunParticles
from modules.MenuHandler import MenuHandler

# -- Core Variables -- #


# -- Core Script -- #

pygame.init() # Initialises pygame and starts it up.
        
screen = pygame.display.set_mode((1472,896)) # Sets the window to 1480 by 900px
isRunning = True # Sets runing to True
HT = TrackHands() # Initialises HandTracking to be used throughout the program.
LG = LevelGenerator(screen) # Initialises the Level Generator and pre generates the sprite images
clock = pygame.time.Clock()

# Initialises the Cursor Class 
cursor = Cursor(100,100, pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\Cursor.png')).convert_alpha(), pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\CursorSelect.png')).convert_alpha(), 0.05, screen)    

# Initialises the Player Class
player = Player(screen, pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/spritesheet.png')).convert_alpha(), 0.6)

# Initialise the Tunneler Class
tunneler = Tunneler(screen, pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\portalA.png')).convert_alpha(), pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\portalB.png')).convert_alpha(), player)

LG.setTunneler(tunneler)

MH = MenuHandler(screen, HT, LG, cursor, player, tunneler, clock, os.path.dirname(os.path.abspath(__file__)))

while isRunning: # While isRunning is set to true
    screen.fill((30,30,30)) # Sets the screen colour to 30,30,30 (Blackish)
    #player.draw()
    
    for event in pygame.event.get(): # Constantly Event Checking.
        if event.type == pygame.QUIT: # If the pygame window is closed.
            isRunning = False # Closes out the while loop by setting isRunning to false.
            pygame.quit() # Quits out of pygame.
            HT.stop() # Stops the hand tracking client.
            break
        
        if event.type == pygame.KEYDOWN: # when a key is pressed
            player.keyDown(event)
            
            if event.key == pygame.K_j:
                tunneler.shootTunnel("A", LG.canCollide)
            elif event.key == pygame.K_l:
                tunneler.shootTunnel("B", LG.canCollide)
            
        elif event.type == pygame.KEYUP: # when a key is released
            player.keyUp(event)
                    
    HT.menuTracking() # Runs update image position
    LG.generateLevel() # Runs the level drawing
    MH.drawCurrentMenu()
    
    RunParticles(screen)
    
    #player.movePlayer(LG.canCollide) # Moves the player 
    tunneler.drawTunnels()
    tunneler.canTunnel(player)
    clock.tick(120)
    
    pygame.display.update() # Updates the display with the new buttons to make sure they all appear.