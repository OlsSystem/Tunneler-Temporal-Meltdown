# ---- Python Modules ---- #
import pygame
from modules.utils.TextLabel import TextLabel

# ---- Custom Modules ---- #


# -- Core Variables -- #


# -- Core Script -- #

# For all core inputs that require checking.
class LevelTimer:

    def __init__(self, screen, LG, x, y, db):
        self.screen = screen
        self.LG = LG
        self.db = db
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

    def saveTimerScore(self, chapterID, levelID):
        Id = f"{chapterID}/{levelID}"
        currentSavedBest = self.db.fetchLevelTime(Id)
        
        if not currentSavedBest:
            self.db.setLevelSpeed(Id, self.currentTime)
        else:
            splitTime = currentSavedBest.split(":")
            savedBestInSeconds = (int(splitTime[0]) * 60) + int(splitTime[1]) + (int(splitTime[2]) / 100)
            currentTimeInSeconds = (self.currentMinute * 60) + self.currentSecond + (self.currentMiliSeconds / 100)
            
            if savedBestInSeconds < currentTimeInSeconds:
                self.db.setLevelSpeed(Id, self.currentTime)
                return "New High Score"
            
        
    def getCurrentTime(self):
        return self.currentTime
        
    # grabs an extra zero if theres the correct amount of digits to format time to XX:XX:XX
    def getExtraZeros(self): 
        extraMiliseconds = ""
        extraSeconds = ""
        extraMinutes = ""
        
        # checks the length of the current time if theres only one it adds an extra zero
        if len(str(abs(self.currentMiliSeconds))) == 1: 
            extraMiliseconds = "0"
            
        if len(str(abs(self.currentSecond))) == 1:
            extraSeconds = "0"
            
        if len(str(abs(self.currentMinute))) == 1:
            extraMinutes = "0"
            
        return extraMiliseconds, extraSeconds, extraMinutes
        

    def handleTimer(self):
        if self.timerActive: # checks for active timer status
            
            # adds on to start the timer
            # every 100 currentMili adds a second and every 60 currentSeconds adds a minute
            self.currentMiliSeconds += 1
            if self.currentMiliSeconds == 100:
                self.currentMiliSeconds = 0
                self.currentSecond += 1
            if self.currentSecond == 60:
                self.currentSecond = 0
                self.currentMinute += 1
        
        extraZeros = self.getExtraZeros() # fetches 0's
            
        # writes out the time and adds in the extra zeros
        self.currentTime = f"{extraZeros[2]}{self.currentMinute}:{extraZeros[1]}{self.currentSecond}:{extraZeros[0]}{self.currentMiliSeconds}"
        self.timer.updateText(self.currentTime) # updates the text.

    def drawTimer(self):
        self.timer.draw()