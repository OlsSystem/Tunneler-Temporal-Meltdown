# ---- Python Modules ---- #
import pygame
from threading import Thread

# ---- Menu Files ---- #
from modules.menus.mainMenu import MainMenu
from modules.menus.loadingScreen import LoadingScreen
from modules.menus.settings import SettingsMenu
from modules.menus.levelSelect import LevelSelect
from modules.menus.levelUI import LevelUI
from modules.menus.pauseMenu import PauseLevelUI

# ---- Initialising Variables ---- # 


class MenuHandler():
    def __init__(self, screen, handTracking, levelGenerator, cursor, player, tunneler, clock, root, Inputs, brightnessHandler):
        # Variables for everything each menu option may require
        self.currentMenu = "Main"
        self.previousMenu = []
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.player = player
        self.tunneler = tunneler
        self.clock = clock
        self.rootDir = root
        self.Inputs = Inputs
    
        # load in every menu class to prepare it.
        self.mainMenu = MainMenu(self.screen, self.HT, self.cursor, self.LG, clock, self.rootDir, tunneler, self.Inputs, self)
        self.loadingScreen = LoadingScreen(self.screen, self.HT, self.cursor, self.LG, clock, self.rootDir, tunneler, self.Inputs, self)
        self.settingsMenu = SettingsMenu(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self, brightnessHandler)
        self.levelSelect = LevelSelect(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self)
        self.levelUi = LevelUI(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self)
        self.levelPause = PauseLevelUI(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self)
        
        # all menus avaliable to use
        self.menuDictionary = {
            "Main": self.mainMenu,
            "Settings": self.settingsMenu,
            "LoadingScreen": self.loadingScreen,
            "LevelSelect": self.levelSelect,
            "LevelUI": self.levelUi,
            "LevelPause": self.levelPause
        }
        
        self.ignoredPreviousMenus = ["LevelUI", "LevelPause"]
        
        self.menuDictionary[self.currentMenu].enableUi()

    # hide current menu function to be written later
    def hideCurrentMenu(self):
        print('hide')
        
    def enablePreviousMenu(self):
        if not self.previousMenu:
            return
        
        previous = self.previousMenu.pop()
        
        self.menuDictionary[previous].enableUi()
        self.currentMenu = previous

    def enableLevel(self, chapterId, levelId):
        # enable the level UI
        # enable level gen
        # enable player n stuff
        # pause ability etc
        hasLoaded = self.LG.loadLevel(chapterId, levelId) 
        if hasLoaded:
            self.enableMenu("LevelUI")               
            print('enable level')
        
    def disableLevel(self):
        # disable the level ui
        # disable level gen
        # disable player n stuff
        self.LG.levelEnded()
        self.enableMenu("LevelSelect")
    
    # menu enabling script
    def enableMenu(self, menuId):
        # checks if the menus found in the menu dictionary
        if self.menuDictionary[menuId]:
            
            if self.currentMenu is not None and self.currentMenu in self.ignoredPreviousMenus:
                self.previousMenu.append(self.currentMenu)

            self.menuDictionary[menuId].enableUi() # enables menu selected
            self.currentMenu = menuId # sets id of the current menu
        
    # drawing on the curernt menu based on self.CurrentMenu.
    def drawCurrentMenu(self):
        self.menuDictionary[self.currentMenu].drawCurrentMenu() # draws selected menu