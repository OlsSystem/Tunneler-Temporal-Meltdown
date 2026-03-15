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


class PauseLevelUI:
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

        # Menu components
        self.title = TextLabel(736, 50, "Game Paused", 64, (255, 255, 255), screen)

        self.settingsButton = TextButton(736, 200, "Settings", 36, Green, screen)
        self.homeButton = TextButton(736, 400, "Return to Menu", 36, Red, screen)
        self.backButton = TextButton(736, 600, "Return to Game", 36, (200, 50, 50), screen)

    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def drawCurrentMenu(self):
        if self.enabled == True:

            self.title.draw()
            self.backButton.draw()
            self.homeButton.draw()
            self.settingsButton.draw()

            for event in pygame.event.get(): # Constantly Event Checking.    
                self.InputHandler.inputCheck(event)
                
                if (event.type == pygame.MOUSEBUTTONDOWN):  # When the event is mouse button and down and event button is 1 (keydown)

                    # draws on the buttons
                    if self.backButton.isClicked(event.pos):
                        self.LG.levelStatus()
                        self.MenuHandler.enableMenu("LevelUI")

                    if self.homeButton.isClicked(event.pos):
                        self.MenuHandler.disableLevel()

                    if self.settingsButton.isClicked(event.pos):
                        self.MenuHandler.enableMenu("Settings")