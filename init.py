# ---- Python Modules ---- #
import cv2
import time
import pygame
import os

# ---- Custom Modules ---- #
from modules.handTracking import TrackHands
from modules.utils.ImageButton import ImageButton
from modules.utils.TextButton import TextButton

# -- Core Variables -- #


# -- Core Script -- #

pygame.init() # Initialises pygame and starts it up.
        
screen = pygame.display.set_mode((1480,900)) # Sets the window to 800 by 500px
isRunning = True # Sets runing to True
HT = TrackHands() # Initialises HandTracking to be used throughout the program.

startButton = TextButton(100, 300, "Start", 38, (255,255,255), screen) # Creates a new Start button
endButton = TextButton(100, 100, "End", 38, (255,255,255), screen) # Creates a new End button

while isRunning: # While isRunning is set to true
    screen.fill((30,30,30)) # Sets the screen colour to 30,30,30 (Blackish)
    startButton.draw() # Draws on the start Button
    endButton.draw() # Draws on the end Button
    for event in pygame.event.get(): # Constantly Event Checking.
        if event.type == pygame.QUIT: # If the pygame window is closed.
            isRunning = False # Closes out the while loop by setting isRunning to false.
            pygame.quit() # Quits out of pygame.
            HT.stop() # Stops the hand tracking client.
            break
                    
        if startButton.isClicked(event): # When the start Buttons clicked 
            print('CLICKED START')
            HT.start() # Opens up the Hand Tracking Client
                    
        if endButton.isClicked(event): # When the end Button clicked
            print('CLICKED END')
            HT.stop() # Closes out the Hand Tracking Client
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # When the event is mouse button and down and event button is 1 (keydown)
            print(event.pos)
                    
                    
    pygame.display.update() # Updates the display with the new buttons to make sure they all appear.