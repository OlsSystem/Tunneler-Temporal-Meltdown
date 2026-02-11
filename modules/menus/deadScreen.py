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


class PlayerDiedScreen:
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
        self.title = TextLabel(736, 50, "You Died", 64, (255, 255, 255), screen)
        
        self.time = TextLabel(736, 300, self.LG.timer.getCurrentTime(), 64, (255,255,255), screen)

        self.restartButton = TextButton(400, 50, "Try Again?", 36, (200, 50, 50), screen)

    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def drawCurrentMenu(self):
        if self.enabled == True:

            # draw on the components
            self.title.draw()
            self.restartButton.draw()
            self.time.updateText(self.LG.timer.getCurrentTime())
            self.time.draw()

            for event in pygame.event.get():  # Constantly Event Checking.
                self.InputHandler.inputCheck(event)

                if (event.type == pygame.MOUSEBUTTONDOWN):  # When the event is mouse button and down and event button is 1 (keydown)

                    if self.restartButton.isClicked(event.pos):
                        self.MenuHandler.restartLevel() # restarts the level when clicked