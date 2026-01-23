# ---- Python Modules ---- #
import pygame
from threading import Thread

# ---- Menu Files ---- #
from modules.menus.mainMenu import MainMenu
from modules.menus.loadingScreen import LoadingScreen
from modules.menus.settings import SettingsMenu

# ---- Initialising Variables ---- # 


class MenuHandler():
    def __init__(self, screen, handTracking, levelGenerator, cursor, player, tunneler, clock, root, Inputs):
        # Variables for everything each menu option may require
        self.currentMenu = "Main"
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
        self.mainMenu = MainMenu(self.screen, self.HT, self.cursor, self.LG, clock, self.rootDir, tunneler, self.Inputs)
        self.loadingScreen = LoadingScreen(self.screen, self.HT, self.cursor, self.LG, clock, self.rootDir, tunneler, self.Inputs)
        self.settingsMenu = SettingsMenu(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs)
        
        # the main menu should enable first. 
        #self.loadingScreen.enableUi()
        #self.mainMenu.enableUi()
        self.settingsMenu.enableUi()

    # hide current menu function to be written later
    def hideCurrentMenu(self):
        print('hide')
    
    # menu enabling script
    def enableMenu(self, menuId):
        if menuId == "Main" and self.currentMenu == "Main":
            return
        
        
        
    # drawing on the curernt menu based on self.CurrentMenu.
    def drawCurrentMenu(self):
        self.settingsMenu.drawCurrentMenu()