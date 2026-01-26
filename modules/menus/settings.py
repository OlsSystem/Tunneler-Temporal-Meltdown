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


class SettingsMenu:
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, InputHandler, MenuHandler, brightnessHandler):
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
        self.brightnessSurface = brightnessHandler

        self.title = TextLabel(736, 50, "Settings", 64, (255, 255, 255), screen)

        # volume slider
        # enable disable music
        # graphics?
        # calibration

        # Settings
        self.volumeSlider = Slider(585, 300, 300, 6, 38, screen, "Volume", 0, 100, 75)     
        self.brightnessSlider = Slider(585, 350, 300, 6, 38, screen, "Brightness", 0, 100, 100)           

        # Apply / Back buttons
        self.applyButton = TextButton(576, 796, "Apply", 36, (0, 200, 0), screen)
        self.backButton = TextButton(896, 796, "Back", 36, (200, 50, 50), screen)

    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def drawCurrentMenu(self):
        if self.enabled == True:

            self.title.draw()
            self.applyButton.draw()
            self.backButton.draw()
            self.volumeSlider.draw()
            self.brightnessSlider.draw()
            
            for event in pygame.event.get():  # Constantly Event Checking.
                self.InputHandler.inputCheck(event)
                self.volumeSlider.isClicked(event)
                
                if self.brightnessSlider.isClicked(event) != False:
                    self.brightnessSurface.set_alpha(int((100 - self.brightnessSlider.fetchValue()) * 2.55))

                if (event.type == pygame.MOUSEBUTTONDOWN):  # When the event is mouse button and down and event button is 1 (keydown)
                    if self.applyButton.isClicked(event.pos):
                        print('apply settings.')
                        pygame.mixer.music.set_volume(self.volumeSlider.fetchValue() / 100)
                        
                    if self.backButton.isClicked(event.pos):
                        self.MenuHandler.enablePreviousMenu()
