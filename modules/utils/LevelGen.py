# ---- Python Modules ---- #
import pygame
import os

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 

class LevelGenerator:
    
    def __init__(self, pygameInstance):
        self.screen = pygameInstance
        self.levelName = None
        self.levelLocation = None
        self.levelsFolder = []
        
    def findLevel(self, levelName):
        