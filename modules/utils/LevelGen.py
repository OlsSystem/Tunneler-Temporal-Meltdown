# ---- Python Modules ---- #
import pygame
import os
import csv

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 

class LevelGenerator:
    
    def __init__(self, pygameInstance):
        self.screen = pygameInstance
        self.levelName = None
        self.levelLocation = None
        self.levelsFolder = []
        
    def findLevel(self, levelName):
        print(levelName)
        
# grid = []
#     with open(file_path, newline="") as f:
#         reader = csv.reader(f)
#         for row in reader:
#             grid.append([tile_map.get(int(code), "unknown") for code in row])
#     return grid