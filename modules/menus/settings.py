# ---- Python Modules ---- #
import pygame
import pygame_menu as pm
import os
from threading import Thread
from modules.utils.ImageButton import ImageButton
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.utils.ToggleSwitch import ToggleSwitch
from modules.utils.DropDowns import DropdownSelect
from modules.utils.RadioButtons import RadioButtons
from modules.Player import Player

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)

# ---- Initialising Variables ---- # 


class SettingsMenu():
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, InputHandler):
        self.enabled = False
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.rootDir = rootDir
        self.clock = clock
        self.tunneler = tunneler
        self.InputHandler = InputHandler
        
        self.title = TextLabel(
            736, 50,
            "Settings",
            64,
            (255, 255, 255),
            screen
        )
        
        # volume slider
        # enable disable music
        # graphics?
        # calibration
        
        self.testToggle = ToggleSwitch(
            350,200,80,30,32,self.screen,"test"
        )
        
        self.applyButton = TextButton(
            576, 796,
            "Apply",
            36,
            (0, 200, 0),
            screen
        )

        self.backButton = TextButton(
            896, 796,
            "Back",
            36,
            (200, 50, 50),
            screen
        )

    def enableUi(self):
        self.enabled = True
        
    def disableUi(self):
        self.enabled = False
        
    def drawCurrentMenu(self):
        if self.enabled == True:
            
            self.title.draw()
            self.applyButton.draw()
            self.backButton.draw()
            self.testToggle.draw()
            
            for event in pygame.event.get(): # Constantly Event Checking.    
                self.InputHandler.inputCheck(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # When the event is mouse button and down and event button is 1 (keydown)
                    print('click')
                    print(self.testToggle.isClicked(event.pos))