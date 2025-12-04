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

# -- Core Variables -- #


# -- Core Script -- #

pygame.init() # Initialises pygame and starts it up.
        
screen = pygame.display.set_mode((960,540)) # Sets the window to 1480 by 900px
isRunning = True # Sets runing to True
HT = TrackHands() # Initialises HandTracking to be used throughout the program.
LG = LevelGenerator(screen) # Initialises the Level Generator and pre generates the sprite images
clock = pygame.time.Clock()

startButton = TextButton(100, 300, "Start", 38, (255,255,255), screen) # Creates a new Start button
endButton = TextButton(100, 100, "End", 38, (255,255,255), screen) # Creates a new End button

testLevelLoad1 = TextButton(300, 100, "Test Level 1", 38, (255,209, 21), screen) 
testLevelLoad2 = TextButton(300, 200, "Test Level 2", 38, (255,209, 21), screen)

testLabel = TextLabel(300,300, "This is a Test Label", 60, (255,0,255), screen) # Creates a new Label
fps = TextLabel(200,100, f'{int(clock.get_fps())}', 40, (255,255,255), screen)

# Initialises the Cursor Class 
cursor = Cursor(100,100, pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\Cursor.png')).convert_alpha(), pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\CursorSelect.png')).convert_alpha(), 0.05, screen)    

# Initialises the Player Class
player = Player(screen, pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/mell.png')).convert_alpha(), 0.6)


#LG.loadLevel("CH1", "LV2")

while isRunning: # While isRunning is set to true
    screen.fill((30,30,30)) # Sets the screen colour to 30,30,30 (Blackish)
    startButton.draw() # Draws on the start Button
    testLevelLoad1.draw()
    testLevelLoad2.draw()
    endButton.draw() # Draws on the end Button
    testLabel.draw() # Draw on the text
    fps.draw()
    player.draw()
    
    fps.updateText(f'{int(clock.get_fps())}')  
    
    if HT.menuTracked and cursor.handMode == "Select":
        if endButton.isClicked(cursor.rectangle.topleft):
            print('CLICKED END')
            HT.stop() # Closes out the Hand Tracking Client
            HT.disableMenuTracking() # Disabes the menu hand tracking.
            LG.levelEnded()
            
        if testLevelLoad2.isClicked(cursor.rectangle.topleft):
            print('CLICKED TEST LOAD 2')
            LG.loadLevel("CH1", "LV2")
            
        if testLevelLoad1.isClicked(cursor.rectangle.topleft):
            print('CLICKED TEST LOAD 1')
            LG.loadLevel("CH1", "LV1")
    
    for event in pygame.event.get(): # Constantly Event Checking.
        if event.type == pygame.QUIT: # If the pygame window is closed.
            isRunning = False # Closes out the while loop by setting isRunning to false.
            pygame.quit() # Quits out of pygame.
            HT.stop() # Stops the hand tracking client.
            break
        
        if event.type == pygame.KEYDOWN: # when a key is pressed
            player.keyDown(event)
        elif event.type == pygame.KEYUP: # when a key is released
            player.keyUp(event)
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # When the event is mouse button and down and event button is 1 (keydown)
            if startButton.isClicked(event.pos): # When the start Buttons clicked 
                print('CLICKED START')
                HT.start() # Opens up the Hand Tracking Client
                HT.enableMenuTracking(cursor) # Enables the menu hand tracking.
                    
            if endButton.isClicked(event.pos): # When the end Button clicked
                print('CLICKED END')
                HT.stop() # Closes out the Hand Tracking Client
                HT.disableMenuTracking() # Disabes the menu hand tracking.
                LG.levelEnded()
            
            print(event.pos)
                    
    HT.menuTracking() # Runs update image position
    LG.generateLevel() # Runs the level drawing
    
    player.movePlayer(LG.canCollide) # Moves the player 
    clock.tick(120)
    pygame.display.update() # Updates the display with the new buttons to make sure they all appear.