# ---- Python Modules ---- #
import pygame
import os
import csv

from modules.utils.LevelDictionary import levelById
from modules.utils.ItemMapping import itemMap, itemImageMap, collisionItems

# ---- Misc Variables ---- #

assetSize = 64

# ---- Initialising Variables ---- # 

class LevelGenerator():
    def __init__(self, pygameInstance):
        self.rootDir = os.path.dirname(__file__) # Root directory of where this file is.
        self.screen = pygameInstance # Add the screen from the main file.
        self.levelName = None # Defines level name
        self.levelPath = None # Defines level path
        self.inLevel = False # Check for if a users in a level
        self.levelLocation = os.path.normpath(os.path.join(self.rootDir, "../levels")) # Normalised path for central level folder
        self.levelsFolder = [] # List of all folders that contains levels.
        self.levelGrid = [] # Creates the level into a grid
        self.levelAssets = {} # Adds all assets that are defined in itemImageMap to a loaded state
        self.canCollide = [] # Lists all items that can be collided with
        self.tunneler = None
        self.player = None
        self.menuHandler = None
        
        self.loadAssets() # Loads all assets to be used in levels.


    def setTunneler(self, tunneler):
        self.tunneler = tunneler
        
    def setPlayer(self, player):
        self.player = player
        
    def setMenuHandler(self, MH):
        self.menuHandler = MH
        
    def loadLevel(self, chapterId, levelId):
        if self.inLevel: # if the users in the level the end the level
            self.levelEnded()
            
        # loadingScreen.enabled() needs creating.
        self.findLevel(chapterId, levelId) # find the level 
        with open(self.levelPath, newline="") as lvl: # opens the csv file of the level requested.
            levelReader = csv.reader(lvl) # changes the csv file into a readable list you can iterate through
            for row in levelReader:
                # needs to allow strings too. <3
                self.levelGrid.append([itemMap.get(int(code), "Unknown") for code in row]) # adds each row of items to the grid
         
        shouldContinue = self.loadStartAndFinish()     
        
        if not shouldContinue:
            self.menuHandler.enableMenu("LevelSelect")
            return False
                
        self.inLevel = True # sets in level to true
        self.tunneler.disableTunnelShooting()
        self.tunneler.enableTunnelShooting()
        
    def levelStatus(self):
        self.inLevel = not self.inLevel
        
    def levelEnded(self): # resets all values to zero ready for the next level
        self.levelGrid = []
        self.canCollide = []
        self.inLevel = False
        self.tunneler.disableTunnelShooting()
        self.tunneler.destoryTunnels()
        
    def loadAssets(self):
        for assetId, filePath in itemImageMap.items(): # iterates through each item in the map
            image = pygame.image.load(os.path.normpath(os.path.join(self.rootDir, f'../{filePath}'))).convert_alpha() # loads the image ready to be used
            code = None # defines that a code is wanted
            for itemCode, itemName in itemMap.items(): # loops through the item map comparing codes to find the correct asset
                if itemName == assetId:
                    code = itemName # sets code to the asset name
            
            if code is not None:   
                self.levelAssets[code] = image # adds the asset and the code into the levelAssets list
            
    def createFinishCoords(self, finishCoords):
        if not finishCoords:
            return 0, 0, 0, 0  

        left = top = float("inf")
        right = bottom = float("-inf")

        for x, y in finishCoords:
            left = min(left, x)
            top = min(top, y)
            right = max(right, x + self.assetSize)
            bottom = max(bottom, y + self.assetSize)

        return left, top, right - left, bottom - top

        
    def loadStartAndFinish(self):
        startX,startY,finishX,finishY,finishW,finishH = 0, 0, 0, 0, 0, 0
        startCount = 0
        finishCoords = []
        finishCount = 0
        for y, row in enumerate(self.levelGrid): # iterates through the grid getting the row and y value
            for x, code in enumerate(row): # iterates through the rows getting a value for x
                if code == "S" and startCount != 1:
                    startX = x * assetSize
                    startY = y * assetSize   
                    startCount += 1
                elif code == "F":
                    boxCoords = (x * assetSize, y * assetSize)
                    finishCoords.append(boxCoords)
                    finishCount += 1  
                elif self.levelGrid.count("F") == finishCount:
                    finishX,finishY,finishW,finishH = self.createFinishCoords(finishCoords)
                    break
                
            if self.levelGrid.count("F") and startCount == 1:
                break
                    
        if startY and startX and finishX and finishY and finishW and finishH:
            self.player.levelStarted(startX, startY, finishX, finishY, finishW, finishH)  
        else:
            print('err')
            return False       
                    
                     
    def generateLevel(self):
        self.canCollide = [] # not having this causes a memory leak
        if self.inLevel: # check that the users in a level before attempting to draw
            for y, row in enumerate(self.levelGrid): # iterates through the grid getting the row and y value
                for x, code in enumerate(row): # iterates through the rows getting a value for x
                    if code == "S" or code == "F":
                        # invis boxes.
                        # start checks if person walks on F 
                        # move player to S levelStarted
                        print('start n finish')
                        
                    elif code in self.levelAssets: 
                        if code in collisionItems: # checks if the item has collisions
                            collisionBox = pygame.Rect(x * assetSize, y * assetSize, assetSize, assetSize) # creates a collision box around it
                            self.canCollide.append(collisionBox) # adds collision box to a list
                            #pygame.draw.rect(self.screen, (200,200,200), collisionBox) # test draw for collision boxes
                            
                        self.screen.blit(self.levelAssets[code], (x * assetSize, y * assetSize)) # draws assets


        # disable loading screen and enable game.
        
    def findLevel(self, chapterId, levelId):
        for chapter in os.listdir(self.levelLocation): # lists out all chapter files in the levels folder
            path = os.path.join(self.levelLocation, chapter) # creates a path to the chapter folder
            
            if os.path.isdir(path) and chapter == chapterId: # checks the folder name against the chapter id
                for level in os.listdir(path): # iterates through the chapter folder
                    levelPath = os.path.join(path, level) # creates a temporary level path

                    if level.split(".")[0] == levelId: # checks the level .csv file is the correct by comparing ids
                        self.levelName = levelById[chapterId][levelId] # level name from the levelById map
                        self.levelPath = levelPath # add the level path to the self