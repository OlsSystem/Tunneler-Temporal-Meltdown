# ---- Python Modules ---- #
import pygame
import time
from threading import Thread
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.utils.TextBox import TextBox

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)

# ---- Initialising Variables ---- #


class NewUser:
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, InputHandler, MenuHandler, brightnessHandler, dataHandler):
        self.enabled = False
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.rootDir = rootDir
        self.clock = clock
        self.tunneler = tunneler
        self.InputHandler = InputHandler
        self.MenuHandler = MenuHandler
        self.brightnessSurface = brightnessHandler
        self.db = dataHandler
        
        self.showError = False

        # Menu components
        self.title = TextLabel(736, 50, "Welcome New User", 64, (255, 255, 255), screen)

        self.inputBox = TextBox(736, 200, 300, 50, 32, screen, placeholder="Enter username...")
        self.errorLabel = TextLabel(736, 700, "", 32, (255, 50, 50), screen)

        self.applyButton = TextButton(736, 796, "Apply", 36, (0, 200, 0), screen)
        
    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False
        
    def hideError(self):
        time.sleep(3)
        self.showError = False

    def drawCurrentMenu(self):
        if self.enabled == True:

            self.title.draw()
            self.inputBox.draw()
            self.applyButton.draw()
            
            if self.showError:
                self.errorLabel.draw()

            for event in pygame.event.get():  # Constantly Event Checking.
                self.InputHandler.inputCheck(event)
                self.inputBox.handle_event(event)
                
                if (event.type == pygame.MOUSEBUTTONDOWN):  # When the event is mouse button and down and event button is 1 (keydown)
                    if self.applyButton.isClicked(event.pos):
                        response = self.db.setNewUserData(self.inputBox.get_value())
                    
                        if response:
                            self.MenuHandler.enableMenu("Main")
                        else:
                            self.errorLabel.updateText("Username already taken.")
                            self.showError = True    
                            Thread(target=self.hideError).start()      
                
            self.inputBox.update()
