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

        self.currentChapter = None  

        self.title = TextLabel(736, 50, "Select a Level", 64, (255, 255, 255), screen)

        self.backButton = TextButton(736, 796, "Back", 36, (200, 50, 50), screen)

        self.chapterButtons = []  
        self.levelButtons = []  

        self.buildChapterButtons()

    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def buildChapterButtons(self):
        self.chapterButtons.clear()
        x = 736
        y = 200
        spacing = 80

        for chapterId, chapterData in levelById.items():
            button = TextButton(x, y, chapterData["name"], 36, (200, 50, 50), self.screen)
            self.chapterButtons.append((chapterId, button))
            y += spacing

    def buildLevelButtons(self, chapterId):
        self.levelButtons.clear()
        x = 736
        y = 200
        spacing = 60

        levels = levelById[chapterId]["levels"]
        for level in levels:
            levelId = level["id"]
            levelName = level["name"]
            button = TextButton(x, y, levelName, 32, (50, 200, 50), self.screen)
            self.levelButtons.append((chapterId, levelId, button))
            y += spacing

    def drawCurrentMenu(self):
        if not self.enabled:
            return

        self.title.draw()
        self.backButton.draw()

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

                if self.backButton.isClicked(mouse_pos):
                    if self.currentChapter is None:
                        self.MenuHandler.enablePreviousMenu()
                    else:
                        self.currentChapter = None
                        self.buildChapterButtons()
                    continue

                if self.currentChapter is None:
                    for chapterId, button in self.chapterButtons:
                        if button.isClicked(mouse_pos):
                            self.currentChapter = chapterId
                            self.buildLevelButtons(chapterId)
                            break
                else:
                    for chapterId, levelId, button in self.levelButtons:
                        if button.isClicked(mouse_pos):
                            self.MenuHandler.enableLevel(chapterId, levelId)
                            break