# ---- Python Modules ---- #
import pygame
import os
import csv

from modules.utils.LevelDictionary import levelById
from modules.utils.ItemMapping import itemMap, itemImageMap, collisionItems, moveableItems

# ---- Misc Variables ---- #

assetSize = 64
moveItemBy = 0.3
stringCodes = ["S", "F"]

# ---- Initialising Variables ---- # 

class LevelGenerator():
    def __init__(self, pygameInstance):
        self.rootDir = os.path.dirname(__file__) # Root directory of where this file is.
        self.screen = pygameInstance # Add the screen from the main file.
        self.levelName = None # Defines level name
        self.chapterId = None # Gives chapter id
        self.levelId = None # Gives level id
        self.levelPath = None # Defines level path
        self.inLevel = False # Check for if a users in a level
        self.levelLocation = os.path.normpath(os.path.join(self.rootDir, "../levels")) # Normalised path for central level folder
        self.levelsFolder = [] # List of all folders that contains levels.
        self.levelGrid = [] # Creates the level into a grid
        self.levelAssets = {} # Adds all assets that are defined in itemImageMap to a loaded state
        self.canCollide = [] # Lists all items that can be collided with
        self.canMove = []
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
                self.levelGrid.append([
                    itemMap.get(int(code) if code.isdigit() else code, "Unknown")
                    for code in row
                ]) 
                
        shouldContinue = self.loadStartAndFinish()
        
        if not shouldContinue:
            self.menuHandler.enableMenu("LevelSelect")
            return False

        self.loadMoveables()
                
        self.inLevel = True # sets in level to true
        self.chapterId = chapterId
        self.levelId = levelId
        self.tunneler.disableTunnelShooting()
        self.tunneler.enableTunnelShooting()
        return True
        
    def levelStatus(self):
        self.inLevel = not self.inLevel
        
    def levelEnded(self): # resets all values to zero ready for the next level
        self.levelGrid = []
        self.canCollide = []
        self.inLevel = False
        self.chapterId = None
        self.levelId = None
        self.tunneler.disableTunnelShooting()
        self.tunneler.destoryTunnels()

    def reloadCurrentLevel(self):
        chapterId = self.chapterId
        levelId = self.levelId
        self.levelEnded()
        return self.loadLevel(chapterId, levelId)
        
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
        print('generating coords')
        if not finishCoords:
            return 0, 0, 0, 0  

        left = top = float("inf")
        right = bottom = float("-inf")

        for x, y in finishCoords:
            left = min(left, x)
            top = min(top, y)
            right = max(right, x + assetSize)
            bottom = max(bottom, y + assetSize)

        return left, top, right - left, bottom - top

        
    def loadStartAndFinish(self):
        startX,startY,finishX,finishY,finishW,finishH = 0, 0, 0, 0, 0, 0
        startCount = 0
        finishCoords = []
        finishCount = 0
        for y, row in enumerate(self.levelGrid): # iterates through the grid getting the row and y value
            print(row)
            for x, code in enumerate(row): # iterates through the rows getting a value for x
                print(code)
                if code == "Spawn" and startCount == 0:
                    startX = x * assetSize
                    startY = y * assetSize   
                    startCount += 1
                elif code == "Finish":
                    boxCoords = (x * assetSize, y * assetSize)
                    finishCoords.append(boxCoords)
                    finishCount += 1
                    
            if finishCount >= 1 and startCount == 1:
                finishX,finishY,finishW,finishH = self.createFinishCoords(finishCoords)
                break
                 
        print(finishCoords)         
        print(startX, startY, finishX, finishY, finishW, finishH)
       
        if startY and startX and finishX and finishY and finishW and finishH:
            self.player.levelStarted(startX, startY, finishX, finishY, finishW, finishH)
            return True 
        else:
            print('err')
            return False       

    def loadMoveables(self):
        self.canMove = [] # prevent memory leaks
        for y, row in enumerate(self.levelGrid):
            for x, code in enumerate(row):
                if code in moveableItems:
                    self.canMove.append({
                        "rect": pygame.Rect(x * assetSize, y * assetSize - 1, assetSize, assetSize),
                        "coordinates": (x * assetSize, y * assetSize - 1),
                        "asset": self.levelAssets[code],
                    })

    def moveMoveable(self, moveableId):
        coordinates = self.canMove[moveableId]["coordinates"]
        asset = self.canMove[moveableId]["asset"]

        new_x = coordinates[0] + moveItemBy * assetSize

        self.canMove[moveableId] = {
            "rect": pygame.Rect(new_x, coordinates[1], assetSize, assetSize),
            "coordinates": (new_x, coordinates[1]),
            "asset": asset,
        }

    def generateLevel(self):
        self.canCollide = [] # not having this causes a memory leak
        if self.inLevel: # check that the users in a level before attempting to draw
            for y, row in enumerate(self.levelGrid): # iterates through the grid getting the row and y value
                for x, code in enumerate(row): # iterates through the rows getting a value for x
                    if code == "Spawn" or code == "Finish":
                        # invis boxes.
                        # start checks if person walks on F 
                        # move player to S levelStarted
                        continue
                    else:
                        if code == None:
                            continue

                        if code in collisionItems: # checks if the item has collisions
                            collisionBox = pygame.Rect(x * assetSize, y * assetSize, assetSize, assetSize) # creates a collision box around it
                            self.canCollide.append(collisionBox) # adds collision box to a list
                            #pygame.draw.rect(self.screen, (200,200,200), collisionBox) # test draw for collision boxes
                            self.screen.blit(self.levelAssets[code], (x * assetSize, y * assetSize)) # draws assets

                        for id, data in enumerate(self.canMove):
                            #self.screen.blit(data["asset"], data["coordinates"])  # draws assets
                            pygame.draw.rect(self.screen, (200,200,200), data["rect"]) # test draw for collision boxes


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