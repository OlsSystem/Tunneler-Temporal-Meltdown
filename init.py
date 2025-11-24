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

pygame.init()
        
screen = pygame.display.set_mode((800,500))
isRunning = True
HT = TrackHands()        

startButton = TextButton(100, 300, "Start", 38, (255,255,255), screen)
endButton = TextButton(100, 100, "End", 38, (255,255,255), screen)

while isRunning:
    screen.fill((30,30,30))
    startButton.draw()
    endButton.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            pygame.quit()
            HT.stop()
            break
                    
        if startButton.isClicked(event):
            print('CLICKED START')
            HT.start()
                    
        if endButton.isClicked(event):
            print('CLICKED END')
            HT.stop()
                    
                    
    pygame.display.update()