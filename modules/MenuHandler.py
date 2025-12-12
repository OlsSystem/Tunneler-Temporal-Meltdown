# ---- Python Modules ---- #
import pygame
from threading import Thread

# ---- Menu Files ---- #
from modules.menus.mainMenu import MainMenu

# ---- Initialising Variables ---- # 


class MenuHandler():
    def __init__(self, screen, handTracking, levelGenerator, cursor, player, tunneler):
        self.currentMenu = "Main"
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.player = player
        self.tunneler = tunneler
    
        self.mainMenu = MainMenu(self.screen, self.HT, self.cursor, self.LG)
        self.mainMenu.enableUi()


    def hideCurrentMenu(self):
        print('hide')
    
    def enableMenu(self, menuId):
        if menuId == "Main" and self.currentMenu == "Main":
            return
        
        
    def drawCurrentMenu(self):
        self.mainMenu.drawCurrentMenu()