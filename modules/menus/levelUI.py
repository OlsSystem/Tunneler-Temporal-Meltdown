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

        self.title = TextLabel(736, 50, "Level", 64, (255, 255, 255), screen)

        self.Pause = TextButton(800, 50, "Pause", 36, (200, 50, 50), screen)


    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def drawCurrentMenu(self):
        if self.enabled == True:

            self.title.draw()
            self.Pause.draw()
            
            self.LG.timer.handleTimer()
            self.LG.timer.drawTimer()
            
            if self.HT.handLocation == "Top Right":
                self.Player.keyUp("Left")
                self.Player.keyDown("Right")
                
            elif self.HT.handLocation == "Top Left":
                self.Player.keyUp("Right")
                self.Player.keyDown("Left")
            
            else:
                self.Player.keyUp("Right")
                self.Player.keyUp("Left")


    
            for event in pygame.event.get(): # Constantly Event Checking.    
                self.InputHandler.inputCheck(event)
                
                if (event.type == pygame.MOUSEBUTTONDOWN):  # When the event is mouse button and down and event button is 1 (keydown)

                    if self.Pause.isClicked(event.pos):
                        self.LG.levelStatus()
                        self.LG.timer.pauseTimer()
                        self.MenuHandler.enableMenu("LevelPause")