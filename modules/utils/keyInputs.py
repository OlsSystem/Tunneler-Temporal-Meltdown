# ---- Python Modules ---- #
import pygame

# ---- Custom Modules ---- #


# -- Core Variables -- #


# -- Core Script -- #

# For all core inputs that require checking.
class KeyInputs:
    
    def __init__(self, HT, tunneler, player, LG):
        self.HT = HT
        self.Tunneler = tunneler
        self.Player = player
        self.LG = LG
        self.isRunning = True
    
    def inputCheck(self, event):
        if event.type == pygame.QUIT: # If the pygame window is closed.
            self.isRunning = False # Closes out the while loop by setting isRunning to false.
            pygame.quit() # Quits out of pygame.
            
            if self.HT.cameraUiEnabled:
                self.HT.stop() # Stops the hand tracking client.
            
            exit()
        
        if event.type == pygame.KEYDOWN: # when a key is pressed
            
            if self.LG.inLevel:
                self.Player.keyDown(event)
            
                if event.key == pygame.K_j:
                    self.Tunneler.shootTunnel("A", self.LG.canCollide)
                elif event.key == pygame.K_l:
                    self.Tunneler.shootTunnel("B", self.LG.canCollide)
            
        elif event.type == pygame.KEYUP: # when a key is released
            if self.LG.inLevel:
                self.Player.keyUp(event)