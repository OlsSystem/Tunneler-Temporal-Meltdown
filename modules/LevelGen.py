# ---- Python Modules ---- #
import pygame
import os
import csv

from modules.utils.LevelDictionary import levelById
from modules.utils.ItemMapping import itemMap, itemImageMap, collisionItems, moveableItems
from modules.utils.Timer import LevelTimer

from modules.gameObjects.button import GameButton
from modules.gameObjects.door import Door

# ---- Misc Variables ---- #

assetSize = 64
moveItemBy = 0.3

# ---- Initialising Variables ---- # 

class LevelGenerator():
    def __init__(self, pygameInstance, handTracking):
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
        self.interactables = []
        self.wildCards = []
        self.canMove = []
        self.tunneler = None
        self.player = None
        self.menuHandler = None
        self.HT = handTracking
        self.timer = LevelTimer(self.screen, self, 400, 50)
        
        self.loadAssets() # Loads all assets to be used in levels.


    def setTunneler(self, tunneler):
        self.tunneler = tunneler
        
    def setPlayer(self, player):
        self.player = player
        
    def setMenuHandler(self, MH):
        self.menuHandler = MH
        
    def fetchCode(self, code):
        if code.isdigit():
            return itemMap.get(int(code), "Unknown")

        if code in itemMap:
            return itemMap[code]

        for key in itemMap:
            if isinstance(key, str) and key.endswith("*"):
                prefix = key[:-1]  # remove the *
                if code.startswith(prefix):
                    return itemMap[key] + code[len(prefix):]

        return "Unknown"
        
    def loadLevel(self, chapterId, levelId):
        if self.inLevel: # if the users in the level the end the level
            self.levelEnded()
            
        # loadingScreen.enabled() needs creating.
        self.findLevel(chapterId, levelId) # find the level 
        with open(self.levelPath, newline="") as lvl: # opens the csv file of the level requested.
            levelReader = csv.reader(lvl) # changes the csv file into a readable list you can iterate through
            for row in levelReader:
                # needs to allow strings too. 
                # needs re writing to all for interaction with the wild cards
                self.levelGrid.append([
                    self.fetchCode(code)
                    for code in row
                ]) 
             
        # loads the start and finish special rects   
        shouldContinue = self.loadStartAndFinish()
        
        # only continues if theres a start and finish
        if not shouldContinue:
            self.menuHandler.enableMenu("LevelSelect")
            return False

        self.loadMoveables() # loads any moveable objects
        self.loadWildCards() # loads any wild card function
        
        self.inLevel = True # sets in level to true
        self.chapterId = chapterId
        self.levelId = levelId
        self.tunneler.disableTunnelShooting()
        self.tunneler.enableTunnelShooting()
        self.HT.start() # Opens up the Hand Tracking Client
        self.timer.startTimer()
        return True
        
    def levelStatus(self):
        # handles turning the timer on and off and setting the level to active and inactive.
        self.inLevel = not self.inLevel
        if not self.inLevel:
            self.timer.pauseTimer()
        else:
            self.timer.startTimer()
        
    def levelEnded(self): # resets all values to zero ready for the next level
        self.levelGrid = []
        self.canCollide = []
        self.interactables = []
        self.wildCards = []
        self.canMove = []
        self.inLevel = False
        self.chapterId = None
        self.levelId = None
        self.timer.pauseTimer() # stops the timer
        self.HT.stop() # stops hand tracking
        
        # resets tunneler logic
        self.tunneler.disableTunnelShooting()
        self.tunneler.destoryTunnels()

    def reloadCurrentLevel(self):
        # resets the chapter and level ids
        chapterId = self.chapterId
        levelId = self.levelId
        self.levelEnded() # ends the level
        self.timer.resetTimer() # restarts the timer
        
        # disables movement and sets x direction to 0
        self.player.isMoving = False
        self.player.isJumping = False
        self.player.x_direction = 0
        
        # loads up the level again
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
        if not finishCoords: # if no finish coords then return 0,0,0,0
            return 0, 0, 0, 0  

        left = top = float("inf") # sets left and top to a positive infinity float
        right = bottom = float("-inf") # sets right and bottom to a negative infinity float

        # loops through the x and y values in the finishCoords to generate the x,y, width and height values
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
            for x, code in enumerate(row): # iterates through the rows getting a value for x
                if code == "Spawn" and startCount == 0: # checks for a spawn and if one has already been generated
                    startX = x * assetSize
                    startY = y * assetSize   
                    startCount += 1
                elif code == "Finish": # checks for a finish block and pushes its coords to a array
                    boxCoords = (x * assetSize, y * assetSize)
                    finishCoords.append(boxCoords)
                    finishCount += 1
                    
            if finishCount >= 1 and startCount == 1: # checks for a finish and start value made then creates the finish x,y,w,h rect
                finishX,finishY,finishW,finishH = self.createFinishCoords(finishCoords)
                break
                        
        if startY and startX and finishX and finishY and finishW and finishH: # makes sure all the values are there before starting the level
            self.player.levelStarted(startX, startY, finishX, finishY, finishW, finishH) # starts the level
            return True 
        else:
            print('err')
            return False    
        
    def loadWildCards(self): # used to link interactables together. ie doors n buttons
        self.wildCards = [] # prevent memory leaks
        for y, row in enumerate(self.levelGrid):
            for x, code in enumerate(row):
                if code == None:
                    continue
                
                if "*" in code: # finds the wildcards
                    wildcardSplit = code.split("*")
                    if "Door" in code:
                        for interactable in self.interactables:
                            if interactable.getId() == wildcardSplit[1]:
                                door = Door(x,y, interactable, self.screen, self.rootDir)
                                self.wildCards.append(door)
                                break
                            
                    if "Button" in code:
                        button = GameButton(self.screen, pygame.Rect(x * assetSize, y * assetSize, assetSize, 16), 16, pygame.Rect(x * assetSize, y * 16, assetSize, 16), wildcardSplit[1], self.levelAssets["Button*"], x, y)
                        self.interactables.append(button)


    def loadMoveables(self):
        self.canMove = [] # prevent memory leaks
        for y, row in enumerate(self.levelGrid):
            for x, code in enumerate(row):
                if code in moveableItems: # places all moveable items into an array with a rect, coordinates, and asset 
                    self.canMove.append({
                        "rect": pygame.Rect(x * assetSize, y * assetSize - 1, assetSize, assetSize),
                        "coordinates": (x * assetSize, y * assetSize - 1),
                        "asset": self.levelAssets[code],
                    })

    def moveMoveable(self, moveableId):
        coordinates = self.canMove[moveableId]["coordinates"] # fetches coordinates
        asset = self.canMove[moveableId]["asset"] # fetches asset

        new_x = coordinates[0] + moveItemBy * assetSize # creates new x value

        self.canMove[moveableId] = { # applies x value to the correct place in the can move array
            "rect": pygame.Rect(new_x, coordinates[1], assetSize, assetSize),
            "coordinates": (new_x, coordinates[1]),
            "asset": asset,
        }

    def generateLevel(self):
        self.canCollide = [] # not having this causes a memory leak
        if self.inLevel: # check that the users in a level before attempting to draw
            for y, row in enumerate(self.levelGrid): # iterates through the grid getting the row and y value
                for x, rawCode in enumerate(row): # iterates through the rows getting a value for x
                    if rawCode == None:
                        continue
                        
                    splitCode = rawCode.split("*")
                    code = splitCode[0]
                    
                    if len(splitCode) > 1:
                        continue
                    
                    if code == "Spawn" or code == "Finish":
                        # invis boxes.
                        # start checks if person walks on F 
                        # move player to S levelStarted
                        continue
                    else:
                        if code in collisionItems: # checks if the item has collisions
                            collisionBox = pygame.Rect(x * assetSize, y * assetSize, assetSize, assetSize) # creates a collision box around it
                            self.canCollide.append(collisionBox) # adds collision box to a list
                            #pygame.draw.rect(self.screen, (200,200,200), collisionBox) # test draw for collision boxes
                            self.screen.blit(self.levelAssets[code], (x * assetSize, y * assetSize)) # draws assets
                        elif code in moveableItems:
                            continue
                        else:   
                            self.screen.blit(self.levelAssets[code], (x * assetSize, y * assetSize)) # draws assets

                for id, data in enumerate(self.canMove):
                    #self.screen.blit(data["asset"], data["coordinates"])  # draws assets
                    pygame.draw.rect(self.screen, (200,200,200), data["rect"]) # test draw for collision boxes
                    
                for wildcard in self.wildCards:
                    wildcard.draw()
                    
                for interactable in self.interactables:
                    interactable.draw()


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