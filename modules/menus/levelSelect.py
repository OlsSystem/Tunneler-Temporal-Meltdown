# ---- Python Modules ---- #
import pygame
import os
from threading import Thread
from modules.utils.ImageButton import ImageButton
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.utils.ToggleSwitch import ToggleSwitch
from modules.utils.DropDowns import DropdownSelect
from modules.utils.RadioButtons import RadioButtons
from modules.utils.Slider import Slider
from modules.Player import Player

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)

# ---- Initialising Variables ---- #


class LevelSelect:
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, InputHandler, MenuHandler):
        self.enabled = False
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.rootDir = rootDir
        self.clock = clock
        self.tunneler = tunneler
        self.InputHandler = InputHandler
        self.MenuHandler = MenuHandler

        self.title = TextLabel(736, 50, "Select a Level", 64, (255, 255, 255), screen)
        
        self.testLevelButton = TextButton(736, 200, "Level 1", 36, (200, 50, 50), screen)

          
        self.backButton = TextButton(736, 796, "Back to Menu", 36, (200, 50, 50), screen)

    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def drawCurrentMenu(self):
        if self.enabled == True:

            self.title.draw()
            self.backButton.draw()
            self.testLevelButton.draw()
            
            for event in pygame.event.get():  # Constantly Event Checking.
                self.InputHandler.inputCheck(event)
                
                if (event.type == pygame.MOUSEBUTTONDOWN):  # When the event is mouse button and down and event button is 1 (keydown)

                    if self.backButton.isClicked(event.pos):
                        self.MenuHandler.enablePreviousMenu()
                        
                    if self.testLevelButton.isClicked(event.pos):
                        self.MenuHandler.enableLevel("CH1", "LV2")
