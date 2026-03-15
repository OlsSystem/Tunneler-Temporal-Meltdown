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
from modules.utils.LevelDictionary import levelById
from modules.menus.menuUtils import buildChapterButtons, buildLevelButtons

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)

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

        # initialises the ui
        self.currentChapter = None  

        self.title = TextLabel(736, 50, "Select a Level", 64, (255, 255, 255), screen)

        self.backButton = TextButton(736, 796, "Back", 36, (200, 50, 50), screen)

        self.chapterButtons = []  
        self.levelButtons = []  

        # builds chapter buttons
        buildChapterButtons(self)

    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def drawCurrentMenu(self):
        if not self.enabled:
            return

        self.title.draw()
        self.backButton.draw()

        # draws on items based on where its at. 
        if self.currentChapter is None:
            for chapterId, button in self.chapterButtons:
                button.draw()
        else:
            for chapterId, levelId, button in self.levelButtons:
                button.draw()

        for event in pygame.event.get():
            self.InputHandler.inputCheck(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # builds chapter buttons if nothings selected
                if self.backButton.isClicked(mouse_pos):
                    if self.currentChapter is None:
                        self.MenuHandler.enablePreviousMenu()
                    else:
                        self.currentChapter = None
                        buildChapterButtons(self)
                    continue

                # builds level buttons if the chapter is selected
                if self.currentChapter is None:
                    for chapterId, button in self.chapterButtons:
                        if button.isClicked(mouse_pos):
                            self.currentChapter = chapterId
                            buildLevelButtons(self, chapterId)
                            break
                else:
                    # enables level selected
                    for chapterId, levelId, button in self.levelButtons:
                        if button.isClicked(mouse_pos):
                            self.MenuHandler.enableLevel(chapterId, levelId)
                            break