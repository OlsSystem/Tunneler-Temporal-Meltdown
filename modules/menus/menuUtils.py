# ---- Python Modules ---- #
import pygame
import time
from threading import Thread
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.utils.TextBox import TextBox
from modules.utils.LevelDictionary import levelById

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)

# ---- Initialising Variables ---- #

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

    for level in levelById[chapterId]["levels"]:
        levelId = level["id"]
        levelName = level["name"]
        button = TextButton(x, y, levelName, 32, (50, 200, 50), self.screen)
        self.levelButtons.append((chapterId, levelId, button))
        y += spacing

def fetchTime(self, timeString):
    mm, ss, cc = timeString.split(":")
    minutes = int(mm)
    seconds = int(ss)
    centis = int(cc)
    return (minutes * 60) + seconds + (centis / 100)