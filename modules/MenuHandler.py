# ---- Python Modules ---- #
import pygame
import math
from threading import Thread
import time
import os

# ---- Menu Files ---- #
from modules.menus.mainMenu import MainMenu
from modules.menus.loadingScreen import LoadingScreen
from modules.menus.settings import SettingsMenu
from modules.menus.levelSelect import LevelSelect
from modules.menus.levelUI import LevelUI
from modules.menus.pauseMenu import PauseLevelUI
from modules.menus.deadScreen import PlayerDiedScreen
from modules.menus.newUser import NewUser
from modules.menus.wonScreen import PlayerWonScreen
from modules.menus.finishGame import PlayerFinishedGame
from modules.menus.leaderboards import LeaderboardMenu

# ---- Initialising Variables ---- #

class MenuHandler():
    def __init__(self, screen, handTracking, levelGenerator, cursor, player, tunneler, clock, root, Inputs, brightnessHandler, dataHandling):
        # Variables for everything each menu option may require
        self.currentMenu = "Main"
        self.previousMenu = []
        self.dataHandler = dataHandling
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.player = player
        self.tunneler = tunneler
        self.clock = clock
        self.rootDir = root
        self.Inputs = Inputs
        
        self.crt_time = 0
        self.ghost_surface = None
    
        # load in every menu class to prepare it.
        self.mainMenu = MainMenu(self.screen, self.HT, self.cursor, self.LG, clock, self.rootDir, tunneler, self.Inputs, self, self.dataHandler)
        self.loadingScreen = LoadingScreen(self.screen, self.HT, self.cursor, self.LG, clock, self.rootDir, tunneler, self.Inputs, self)
        self.settingsMenu = SettingsMenu(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self, brightnessHandler)
        self.levelSelect = LevelSelect(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self)
        self.levelUi = LevelUI(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self, self.player)
        self.levelPause = PauseLevelUI(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self)
        self.deadScreen = PlayerDiedScreen(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self)
        self.newUser = NewUser(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self, brightnessHandler, self.dataHandler)
        self.wonScreen = PlayerWonScreen(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self)
        self.finishedScreen = PlayerFinishedGame(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self)
        self.leaderboard = LeaderboardMenu(self.screen, self.HT, self.cursor, self.LG, self.clock, self.rootDir, self.tunneler, self.Inputs, self, brightnessHandler, self.dataHandler)

        # all menus available to use
        self.menuDictionary = {
            "Main": self.mainMenu,
            "Settings": self.settingsMenu,
            "LoadingScreen": self.loadingScreen,
            "LevelSelect": self.levelSelect,
            "LevelUI": self.levelUi,
            "LevelPause": self.levelPause,
            "DeadScreen": self.deadScreen,
            "NewUser": self.newUser,
            "WinScreen": self.wonScreen,
            "FinishedGame": self.finishedScreen,
            "Leaderboard": self.leaderboard
        }
        
        self.ignoredPreviousMenus = ["LevelUI", "DeadScreen", "LoadingScreen", "NewUser", "WinScreen", "FinishedGame"]
        
        self.menuDictionary[self.currentMenu].enableUi()
        
    def draw_scanlines(self, surface, spacing=4, opacity=40):
        # draws on lines with a spacing provided
        width, height = surface.get_size()
        line = pygame.Surface((width, 1))
        line.set_alpha(opacity)
        line.fill((0, 0, 0))
        # loop through the amount of lines 
        for y in range(0, height, spacing):
            surface.blit(line, (0, y))
    
    def draw_ghosting(self):
        # draws on the ghosting effect to the screen
        self.ghost_surface = pygame.transform.smoothscale(self.screen, (1472, 896))
        self.ghost_surface.set_alpha(40)
        self.screen.blit(self.ghost_surface, (1, 0)) 

    # hide current menu function to be written later
    def hideCurrentMenu(self):
        print('hide')
        
    def enablePreviousMenu(self):
        if not self.previousMenu:
            return
        
        previous = self.previousMenu.pop() # drop the previous menu just selected from the list 
        
        self.menuDictionary[previous].enableUi() # enables the dropped previous menu from the list
        self.currentMenu = previous # sets current menu to the previous

    def restartLevel(self):
        # reload level.
        hasLoaded = self.LG.reloadCurrentLevel() 
        if hasLoaded: # starts the level once its loaded.
            self.enableMenu("LevelUI")
            print('reloaded level')
            
    def nextLevel(self):
        currentChapter, currentLevel = self.dataHandler.fetchCurrentLevel().split("/")
        chapterPath = os.path.join(os.path.join(self.rootDir, "levels"), currentChapter)
        
        allLevels = [
            lvl for lvl in os.listdir(chapterPath)
            if lvl.startswith("LV") and lvl.endswith(".csv")
        ]
        
        allLevels.sort(key=lambda lvl: int(lvl.replace("LV", "").replace(".csv", "")))
        currentLevelIndex = allLevels.index(f"{currentLevel}.csv")
        
        if currentLevelIndex == -1:
            print('errr cant find lvl index')
            self.enableMenu("LevelSelect")
            return
            
        if currentLevelIndex + 1 < len(allLevels):
            self.LG.levelEnded()
            self.enableLevel(currentChapter, allLevels[currentLevelIndex + 1])
        else:
            allChapters = [
                chp for chp in os.listdir(os.path.join(self.rootDir, "levels"))
                if chp.startswith("CH")
            ]
            allChapters.sort(key= lambda chp: int(chp.replace("CH", "")))
            currentChapterIndex = allChapters.index(f"{currentChapter}")
            
            if currentChapterIndex == -1:
                print("err cant find chp index")
                self.enableMenu("LevelSelect")
                return
                
            if currentChapterIndex + 1 < len(allChapters):
                print(allChapters[currentChapterIndex + 1], "LV1")
                self.LG.levelEnded()
                self.enableLevel(allChapters[currentChapterIndex + 1], "LV1")
            else:
                self.enableMenu("FinishedGame")
    
    def enableLevel(self, chapterId, levelId):
        # starts the level loading process as a thread to allow for extra while loops to check for the camera.
        self.enableMenu("LoadingScreen")
        Thread(target=self.startLevel(chapterId,levelId)).start()

    def startLevel(self, chapterId, levelId):
        # enable the level UI
        # enable level gen
        # enable player n stuff
        # pause ability etc
        self.dataHandler.setCurrentLevel(f"{chapterId}/{levelId}")
        hasLoaded = self.LG.loadLevel(chapterId, levelId)
        
        while self.HT.checkCamera() == False:
            self.HT.checkCamera()
            if self.HT.checkCamera() == True:
                break
        
        # checks that the levels loaded and the cameras on.
        if hasLoaded and self.HT.checkCamera() == True:
            self.enableMenu("LevelUI")               
        
    def disableLevel(self):
        # disable the level ui
        # disable level gen
        # disable player n stuff
        self.LG.levelEnded()
        self.enableMenu("LevelSelect")

        for code in self.previousMenu:
            if code == "LevelPause":
                self.previousMenu.remove("LevelPause")
    
    # menu enabling script
    def enableMenu(self, menuId):
        # checks if the menus found in the menu dictionary
        if self.menuDictionary[menuId]:
            
            if self.currentMenu is not None and self.currentMenu not in self.ignoredPreviousMenus:
                self.previousMenu.append(self.currentMenu)

            if menuId == "DeadScreen":
                self.LG.levelStatus()
                self.LG.levelCompleated = True
                
            if menuId == "WinScreen":
                self.LG.levelStatus()
                self.LG.levelCompleated = True

            self.menuDictionary[menuId].enableUi() # enables menu selected
            self.currentMenu = menuId # sets id of the current menu
                    
    # drawing on the curernt menu based on self.CurrentMenu.
    def drawCurrentMenu(self):
        # ---- CRT Effect for the main Menu ---- #
        if self.currentMenu != "LevelUI":
            if self.currentMenu != "Settings" or self.currentMenu != "NewUser":
                self.draw_ghosting() # draw the ghost effect
            else:
                self.ghost_surface.fill((0,0,0))
                
            self.draw_scanlines(self.screen) # draws on the lies accross the screen
            
            # add a green tint to the screen
            tint = pygame.Surface(self.screen.get_size())
            tint.fill((0, 40, 20))  
            tint.set_alpha(20)
            self.screen.blit(tint, (0, 0))
        else:
            self.screen.fill((30,30,30)) # Sets the screen colour to 30,30,30 (Blackish)
        
        self.menuDictionary[self.currentMenu].drawCurrentMenu() # draws selected menu