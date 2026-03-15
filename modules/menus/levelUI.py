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


class LevelUI:
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, InputHandler, MenuHandler, Player):
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
        self.Player = Player
        
        # Menu components
        self.levelName = TextLabel(
            736, 30,
            self.LG.levelName,
            36,
            (255, 255, 255),
            screen
        )

        self.Pause = TextButton(
            0, 0,
            "Pause",
            40,
            (220, 80, 80),
            screen
        )



    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def drawCurrentMenu(self):
        if not self.enabled:
            return

        pygame.draw.rect(self.screen, (20, 20, 20), (0, 0, 1472, 120))
        pygame.draw.line(self.screen, (80, 80, 80), (0, 120), (1472, 120), 2)

        name_h = self.levelName.render.get_height()
        self.levelName.x = (1472 // 2) 
        self.levelName.y = 30 

        self.Pause.rectangle.centerx = 1472 // 2
        self.Pause.rectangle.centery = 30 + name_h + 25 
        self.levelName.updateText(self.LG.levelName)
        
        self.levelName.draw()
        self.Pause.draw()

        self.LG.timer.handleTimer()
        self.LG.timer.drawTimer()

        if self.HT.handLocation == "Top Right":
            self.Player.keyUp("Left")
            self.Player.keyDown("Right")
        elif self.HT.handLocation == "Top Left":
            self.Player.keyUp("Right")
            self.Player.keyDown("Left")
        elif self.HT.handLocation in ("Bottom Left", "Bottom Right"):
            self.Player.keyDown("Jump")
            self.Player.keyUp("Right")
            self.Player.keyUp("Left")
        else:
            self.Player.keyUp("Right")
            self.Player.keyUp("Left")

        for event in pygame.event.get():
            self.InputHandler.inputCheck(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.Pause.isClicked(event.pos):
                    self.LG.levelStatus()
                    self.MenuHandler.enableMenu("LevelPause")