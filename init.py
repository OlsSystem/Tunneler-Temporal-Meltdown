# ---- Python Modules ---- #
import time
import pygame
import os

# ---- Custom Modules ---- #
from modules.utils.ImageButton import ImageButton
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.utils.Cursor import Cursor
from modules.utils.keyInputs import KeyInputs
from modules.utils.Particles import RunParticles

from modules.LevelGen import LevelGenerator
from modules.Player import Player
from modules.handTracking import TrackHands
from modules.MenuHandler import MenuHandler

from modules.Items.Tunneler import Tunneler

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
player = Player(screen, pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\spritesheet.png')).convert_alpha(), 0.6)

# Initialise the Tunneler Class
tunneler = Tunneler(screen, pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\portalA.png')).convert_alpha(), pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\portalB.png')).convert_alpha(), player)

LG.setTunneler(tunneler)
InputHandler = KeyInputs(HT, tunneler, player, LG, True)

brightnessSurface = pygame.Surface(screen.get_size())
brightnessSurface.set_alpha(int((100 - 100) * 2.55))


MH = MenuHandler(screen, HT, LG, cursor, player, tunneler, clock, os.path.dirname(os.path.abspath(__file__)), InputHandler, brightnessSurface)

while isRunning: # While isRunning is set to true
    screen.fill((30,30,30)) # Sets the screen colour to 30,30,30 (Blackish)
    brightnessSurface.fill((0,0,0))
    player.draw(LG.inLevel)    
    MH.drawCurrentMenu()
    screen.blit(brightnessSurface, (0,0))
                    
    HT.menuTracking() # Runs update image position
    LG.generateLevel() # Runs the level drawing
    
    RunParticles(screen)
    
    player.movePlayer(LG.canCollide, LG.inLevel) # Moves the player 
    tunneler.drawTunnels()
    tunneler.canTunnel(player)
    clock.tick(120)
    pygame.display.update() # Updates the display with the new buttons to make sure they all appear.
