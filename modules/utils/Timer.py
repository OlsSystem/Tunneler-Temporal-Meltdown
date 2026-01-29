# ---- Python Modules ---- #
import pygame
from modules.utils.TextLabel import TextLabel

# ---- Custom Modules ---- #


# -- Core Variables -- #


# -- Core Script -- #

# For all core inputs that require checking.
class LevelTimer:

    def __init__(self, screen, LG, x, y):
        self.screen = screen
        self.LG = LG

        self.timerStatus = False
        self.currentTime = "0:00:000"

        self.timer = TextLabel(x,y,self.currentTime, 38, (255,255,0), self.screen)

    def startTimer(self):
        self.timerStatus = True

    def pauseTimer(self):
        self.timerStatus = False

    def resetTimer(self):
        self.currentTime = "0:00:000"

    def saveTimerScore(self, levelID):
        print('level time saved')

    def handleTimer(self):
        newTime = "test"
        self.timer.updateText(newTime)

    def drawTimer(self):
        if self.timerStatus:
            self.timer.draw()