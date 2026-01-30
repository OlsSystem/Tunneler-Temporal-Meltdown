# ---- Python Modules ---- #
import pygame
from modules.utils.TextLabel import TextLabel

# ---- Custom Modules ---- #


# -- Core Variables -- #


# -- Core Script -- #

#https://www.geeksforgeeks.org/python/create-stopwatch-using-python/

# For all core inputs that require checking.
class LevelTimer:

    def __init__(self, screen, LG, x, y):
        self.screen = screen
        self.LG = LG

        self.timerStatus = False
        self.currentMinute = 00
        self.currentSecond = 00
        self.currentHour = 0

        self.currentTime = f"{self.currentHour}:{self.currentMinute}:{self.currentSecond}"

        self.timer = TextLabel(x,y,self.currentTime, 38, (255,255,0), self.screen)

    def startTimer(self):
        self.timerStatus = True

    def pauseTimer(self):
        self.timerStatus = False

    def resetTimer(self):
        self.currentHour = 0
        self.currentMinute = 00
        self.currentSecond = 000

    def saveTimerScore(self, levelID):
        print('level time saved')

    def handleTimer(self):
        newTime = "test"
        self.timer.updateText(newTime)

    def drawTimer(self):
        self.timer.draw()