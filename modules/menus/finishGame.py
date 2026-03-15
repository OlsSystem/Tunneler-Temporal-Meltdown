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
from modules.utils.Timer import LevelTimer

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)


# ---- Initialising Variables ---- #


class PlayerFinishedGame:
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, InputHandler,
                 MenuHandler):
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
        self.title = TextLabel(736, 50, "You Have Compleated the Game!", 64, (255, 255, 255), screen)
        
        self.home = TextButton(400, 50, "Home?", 36, (200, 50, 50), screen)

    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def drawCurrentMenu(self):
        if not self.enabled:
            return

        title_h = self.title.render.get_height()
        self.title.x = (1472 // 2)
        self.title.y = 180

        self.home.rectangle.centerx = 1472 // 2
        self.home.rectangle.centery = self.title.y + title_h + 120

        # Draw UI elements
        self.title.draw()
        self.home.draw()

        # Event handling
        for event in pygame.event.get():
            self.InputHandler.inputCheck(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.home.isClicked(event.pos):
                    self.MenuHandler.enableMenu("Main")