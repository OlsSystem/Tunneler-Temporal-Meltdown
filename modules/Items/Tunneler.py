# ---- Python Modules ---- #
import pygame
from threading import Thread
import time
from modules.utils.Particles import Dust, dustParticles
# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 
threshold = 138 # threshold for teleporting a person with a tunnel

class Tunneler():
    def __init__(self, screen, tunnelAImg, tunnelBImg, player):
        # Initialising Variables used within the class
        self.screen = screen
        self.tunnelA = tunnelAImg
        self.tunnelB = tunnelBImg
        self.player = player
        self.collisions = None
        self.threashold = None
        
        self.tunnelAPlaced = False
        self.tunnelBPlaced = False
        self.currentTunnel = None 
        self.tunnelALoc = None
        self.tunnelARect = None
        self.tunnelBLoc = None
        self.tunnelBRect = None
        self.tunnelAColour = (111, 49, 152)
        self.tunnelBColour = (0, 173, 173)
        self.direction = None
        
        self.tunnelActive = False
        self.canShootTunnels = False
        self.debounce = False
        
        
    def destoryTunnels(self):
        # Destroys all tunnels to "reset a level"
        self.tunnelAPlaced = False
        self.tunnelBPlaced = False
        self.tunnelALoc = None
        self.tunnelBLoc = None
        
        self.tunnelActive = False
        
    def destoryTunnel(self, tunnelCode): 
        if tunnelCode == "A": # disables and destroys tunnel A
            self.tunnelAPlaced = False
            self.tunnelALoc = None
        
            self.tunnelActive = False
        elif tunnelCode == "B": # disables and destroys tunnel B
            self.tunnelBPlaced = False
            self.tunnelBLoc = None
        
            self.tunnelActive = False
        
    def canTunnel(self, player): # maybe do a left threshold and a right threshold??
        # player should spawn as close as possible to the tunnel
        
        if self.tunnelActive: # Checks that the tunnels are online
            if self.tunnelAPlaced and self.tunnelBPlaced: # Checks if both tunnels are placed
                
                if player.rectangle.colliderect(self.tunnelARect): # Checks for collisions
                    xB,yB = self.tunnelBLoc # Gatheres x and y coordinates for the tunnel
                    
                    # Changes the teleporting x values depending on the way it faces.
                    if self.player.Facing == "Left":
                        xB -= threshold
                    elif self.player.Facing == "Right":
                        xB += threshold
                        
                    player.tunnelPlayer(xB, yB - 43, self.tunnelBColour) # Teleports the player over to the other tunnel.
            
                if player.rectangle.colliderect(self.tunnelBRect):
                    xA,yA = self.tunnelALoc
                    if self.player.Facing == "Left":
                        xA -= threshold
                    elif self.player.Facing == "Right":
                        xA += threshold
                    player.tunnelPlayer(xA, yA - 43, self.tunnelAColour)

        
    def drawTunnels(self):
        if self.tunnelActive: # only draws if tunnels if one or multiple tunnels are active
            
            # maybe do the drawing x based on if its left or right????
            if self.tunnelAPlaced: # checks if tunnel is placed 
                xA,yA = self.tunnelALoc # pulls coordinates from storage
                self.tunnelARect = pygame.Rect(xA - 10, yA - 20, 20, 86) # creates a rectangle to be used.
                pygame.draw.rect(self.screen, self.tunnelAColour, self.tunnelARect) # draws on the rectangle and correct tunnel colour
                
            if self.tunnelBPlaced:
                xB,yB = self.tunnelBLoc
                self.tunnelBRect = pygame.Rect(xB - 10, yB - 20, 20, 86)
                pygame.draw.rect(self.screen, self.tunnelBColour, self.tunnelBRect)
        
    def enableTunnelShooting(self):
        self.canShootTunnels = True # enables tunnel shooting
        
    def disableTunnelShooting(self):
        self.canShootTunnels = False # disables tunnel shooting
        
    def setTunnelDirection(self): 
        # sets the direction that the pellet should move in.   
        if self.player.Facing == "Left":
            self.direction = -0.004
        elif self.player.Facing == "Right":
            self.direction = 0.004

    def movePellet(self):
        self.x = self.player.rectangle.x # gatheres x of the player 
        colour = (255,255,255) # default colour
        
        # sets pellet colour based on which tunnel was shot
        if self.currentTunnel == "A":
            colour = self.tunnelAColour
        elif self.currentTunnel == "B":
            colour = self.tunnelBColour
        else:
            colour = (255,255,255)
            
            
        while not self.hitWall: # while the wall hasnt been hit
            self.x += self.direction # adds on the direction to the pellet so it moves towards a wall.
            self.energyPellet = pygame.draw.circle(self.screen, colour, (self.x, self.player.rectangle.y + 50), 7) # draws on the pellet to the screen
            rect = pygame.Rect(self.energyPellet.left, self.energyPellet.top, self.energyPellet.width, self.energyPellet.height) # creates a rect around the ball to check for collisions
            for collidables in self.collisions: # checks the collisions from the wall collisions in the level gen
                if rect.colliderect(collidables): # checks if the pellet is touching the wall 
                    print(f'({self.energyPellet.x}, {self.energyPellet.y})')
                    self.hitWall = True # sets that the walls been hit
                    break
        
        # checks what tunnel has been enabled.
        if self.currentTunnel == "A":
            temp = (self.energyPellet.x, self.energyPellet.y) # temp variable for the x,y coordinates of the pellet
            if temp == self.tunnelALoc or temp == self.tunnelBLoc: # if theres already a tunnel at the fired location then it wont place
                print('test')
            else:
                self.tunnelALoc = (self.energyPellet.x, self.energyPellet.y) # sets the new location of the tunnels coordinates
                self.tunnelAPlaced = True # sets A to be placed.
                
            particles = Dust((self.energyPellet.x, self.energyPellet.y), self.tunnelAColour, self.player.Facing) # shoots off particles in the correct direction to the tunnel
            dustParticles.append(particles) # add the particles to the dust list.
        elif self.currentTunnel == "B":
            temp = (self.energyPellet.x, self.energyPellet.y)
            if temp == self.tunnelALoc or temp == self.tunnelBLoc:
                print('test')
            else:
                self.tunnelBLoc = (self.energyPellet.x, self.energyPellet.y)
                self.tunnelBPlaced = True
                
            particles = Dust((self.energyPellet.x, self.energyPellet.y), self.tunnelBColour, self.player.Facing)
            dustParticles.append(particles)

            
        self.tunnelActive = True # sets tunnels active to true
        self.drawTunnels() # starts the drawing process
        self.currentTunnel = None # sets the current tunnel to none.
        self.debounce = False # disables the debounce to stop memory leaks, frame drops, and to prevent lag
        
    def shootTunnel(self, tunnelCode, collisions): # what ever way they are facing fire a tunnel to the closest wall till a collision
        # display a fire like animation and then run place 
        if not self.debounce: # checks if theres already a ball being shot via the debounce variable.
            self.debounce = True # sets debounce to true to stop any extra balls being shot
            if self.canShootTunnels: # checks if tunnels can be shot
                self.currentTunnel = tunnelCode # sets the current tunnel to the tunnel being shot 
                self.setTunnelDirection() # finds the direction the tunnel should be heading in.
                self.collisions = collisions # pulls collisions from the player
                self.energyPellet = pygame.draw.circle(self.screen, self.tunnelAColour, (self.player.rectangle.x, self.player.rectangle.y), 7) # draws on the pellet

                self.hitWall = False # sets wall being hit to false as its not been hit
                Thread(target=self.movePellet).start() # starts a new thread to move the pellet along.
            else:
                self.debounce = False # sets debounce to false as the pellet doesnt move.
            
