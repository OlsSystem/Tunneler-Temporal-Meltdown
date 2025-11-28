# ---- Python Modules ---- #
import pygame
import os
import csv

from modules.utils.LevelDictionary import levelById
from modules.utils.ItemMapping import itemMap, itemImageMap

# ---- Misc Variables ---- #

assetSize = 64

# ---- Initialising Variables ---- # 

class LevelGenerator:
    def __init__(self, pygameInstance):
        self.rootDir = os.path.dirname(__file__)
        self.screen = pygameInstance
        self.levelName = None
        self.levelPath = None
        self.inLevel = False
        self.levelLocation = os.path.normpath(os.path.join(self.rootDir, "../levels"))
        self.levelsFolder = []
        self.levelGrid = []
        self.levelAssets = {}
        
        self.loadAssets()

        
    def loadLevel(self, chapterId, levelId):
        # loadingScreen.enabled()
        self.findLevel(chapterId, levelId)
        with open(self.levelPath, newline="") as lvl:
            levelReader = csv.reader(lvl)
            for row in levelReader:
                self.levelGrid.append([itemMap.get(int(code), "Unknown") for code in row])
                
        self.inLevel = True
        
    def levelEnded(self):
        self.levelGrid = []
        self.inLevel = False
        
    def loadAssets(self):
        for assetId, filePath in itemImageMap.items():
            image = pygame.image.load(os.path.normpath(os.path.join(self.rootDir, f'../{filePath}'))).convert_alpha()
            code = None
            for itemCode, itemName in itemMap.items():
                if itemName == assetId:
                    code = itemName
            
            if code is not None:   
                self.levelAssets[code] = image
                    
    def generateLevel(self):
        if self.inLevel:
            for y, row in enumerate(self.levelGrid):
                for x, code in enumerate(row):
                    if code in self.levelAssets:
                        self.screen.blit(self.levelAssets[code], (x * assetSize, y * assetSize))
                    #elif code == 1:
                    #    pygame.draw.rect(self.screen, (200,200,200),(x * assetSize, y * assetSize, assetSize, assetSize))


        # disable loading screen and enable game.
        
    def findLevel(self, chapterId, levelId):
        for chapter in os.listdir(self.levelLocation):
            path = os.path.join(self.levelLocation, chapter)
            
            if os.path.isdir(path) and chapter == chapterId:
                for level in os.listdir(path):
                    levelPath = os.path.join(path, level)

                    if level.split(".")[0] == levelId:
                        self.levelName = levelById[chapterId][levelId]
                        self.levelPath = levelPath
                        
        
        
        
# grid = []
#     with open(file_path, newline="") as f:
#         reader = csv.reader(f)
#         for row in reader:
#             grid.append([tile_map.get(int(code), "unknown") for code in row])
#     return grid