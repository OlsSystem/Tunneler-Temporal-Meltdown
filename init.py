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

# -- Core Variables -- #


# -- Core Script -- #

pygame.init() # Initialises pygame and starts it up.
        
screen = pygame.display.set_mode((1480,900)) # Sets the window to 1480 by 900px
isRunning = True # Sets runing to True
HT = TrackHands() # Initialises HandTracking to be used throughout the program.
LG = LevelGenerator(screen)
clock = pygame.time.Clock()

startButton = TextButton(100, 300, "Start", 38, (255,255,255), screen) # Creates a new Start button
endButton = TextButton(100, 100, "End", 38, (255,255,255), screen) # Creates a new End button

testLevelLoad = TextButton(300, 200, "Test Level", 38, (255,209, 21), screen)

testLabel = TextLabel(300,300, "This is a Test Label", 60, (255,0,255), screen)

cursor = Cursor(100,100, pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\Cursor.png')).convert_alpha(), pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets\CursorSelect.png')).convert_alpha(), 0.05, screen)    

while isRunning: # While isRunning is set to true
    screen.fill((30,30,30)) # Sets the screen colour to 30,30,30 (Blackish)
    startButton.draw() # Draws on the start Button
    testLevelLoad.draw()
    endButton.draw() # Draws on the end Button
    testLabel.draw() # Draw on the text
    
    if HT.menuTracked and cursor.handMode == "Select":
        if endButton.isClicked(cursor.rectangle.topleft):
            print('CLICKED END')
            HT.stop() # Closes out the Hand Tracking Client
            HT.disableMenuTracking() # Disabes the menu hand tracking.
            
        if testLevelLoad.isClicked(cursor.rectangle.topleft):
            print('CLICKED TEST LOAD')
            LG.loadLevel("CH1", "LV2")
    
    for event in pygame.event.get(): # Constantly Event Checking.
        if event.type == pygame.QUIT: # If the pygame window is closed.
            isRunning = False # Closes out the while loop by setting isRunning to false.
            pygame.quit() # Quits out of pygame.
            HT.stop() # Stops the hand tracking client.
            break
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # When the event is mouse button and down and event button is 1 (keydown)
            if startButton.isClicked(event.pos): # When the start Buttons clicked 
                print('CLICKED START')
                HT.start() # Opens up the Hand Tracking Client
                HT.enableMenuTracking(cursor) # Enables the menu hand tracking.
                    
            if endButton.isClicked(event.pos): # When the end Button clicked
                print('CLICKED END')
                HT.stop() # Closes out the Hand Tracking Client
                HT.disableMenuTracking() # Disabes the menu hand tracking.
            
            print(event.pos)
                    
    HT.menuTracking() # Runs update image position
    pygame.display.update() # Updates the display with the new buttons to make sure they all appear.