# ---- Python Modules ---- #
import pygame
from threading import Thread

# ---- Menu Files ---- #
from modules.menus.mainMenu import MainMenu
from modules.menus.loadingScreen import LoadingScreen
from modules.menus.settings import SettingsMenu

# ---- Initialising Variables ---- # 


class MenuHandler():
    def __init__(self, screen, handTracking, levelGenerator, cursor, player, tunneler, clock, root, Inputs, brightnessHandler):
        # Variables for everything each menu option may require
        self.currentMenu = "Test"
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
        
        # all menus avaliable to use
        self.menuDictionary = {
            "Main": self.mainMenu,
            "Settings": self.settingsMenu,
            "LoadingScreen": self.loadingScreen,
        }
        
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

    
    # menu enabling script
    def enableMenu(self, menuId):
        # checks if the menus found in the menu dictionary
        if self.menuDictionary[menuId]:
            
            if self.currentMenu is not None:
                self.previousMenu.append(self.currentMenu)

            self.menuDictionary[menuId].enableUi() # enables menu selected
            self.currentMenu = menuId # sets id of the current menu
        
    # drawing on the curernt menu based on self.CurrentMenu.
    def drawCurrentMenu(self):
        self.menuDictionary[self.currentMenu].drawCurrentMenu() # draws selected menu