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

        self.timerActive = False
        self.currentMiliSeconds = 0
        self.currentMinute = 0
        self.currentSecond = 0

        self.currentTime = f"{self.currentMinute}:{self.currentSecond}:{self.currentMiliSeconds}"

        self.timer = TextLabel(x,y,self.currentTime, 38, (255,255,0), self.screen)

    def startTimer(self):
        self.timerActive = True

    def pauseTimer(self):
        self.timerActive = False

    def resetTimer(self):
        self.currentMiliSeconds = 0
        self.currentMinute = 0
        self.currentSecond = 0

    def saveTimerScore(self, levelID):
        print('level time saved')
        
    def getCurrentTime(self):
        return self.currentTime
        
    def getExtraZeros(self):
        extraMiliseconds = ""
        extraSeconds = ""
        extraMinutes = ""
        
        if len(str(abs(self.currentMiliSeconds))) == 1: 
            extraMiliseconds = "0"
            
        if len(str(abs(self.currentSecond))) == 1:
            extraSeconds = "0"
            
        if len(str(abs(self.currentMinute))) == 1:
            extraMinutes = "0"
            
        return extraMiliseconds, extraSeconds, extraMinutes
        

    def handleTimer(self):
        if self.timerActive:
            self.currentMiliSeconds += 1
            if self.currentMiliSeconds == 100:
                self.currentMiliSeconds = 0
                self.currentSecond += 1
            if self.currentSecond == 60:
                self.currentSecond = 0
                self.currentMinute += 1
        
        extraZeros = self.getExtraZeros()
            
        self.currentTime = f"{extraZeros[2]}{self.currentMinute}:{extraZeros[1]}{self.currentSecond}:{extraZeros[0]}{self.currentMiliSeconds}"
        self.timer.updateText(self.currentTime)

    def drawTimer(self):
        self.timer.draw()