# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class GameButton():
    def __init__(self, mainButtonRect, buttonHeight, buttonRect):
        # take in all data needed like coords n that shit
        # create a rect around the red of the button
        # check if a moveable is on top
        # if it is set pressed to true
        # if it aint on it set pressed to false
        # if the player is colliding with the button enable it same for if a moveable object is on top
        self.buttonMain = mainButtonRect
        self.height = buttonHeight
        self.button = buttonRect
        self.isPressed = False
        
        
    def beenPressed(self):
        return self.isPressed