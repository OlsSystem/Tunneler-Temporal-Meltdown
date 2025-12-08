# ---- Python Modules ---- #
import pygame
from threading import Thread
import time
# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 
threshold = 138

class Tunneler():
    def __init__(self, screen, tunnelAImg, tunnelBImg, player):
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
        self.tunnelAColour = (255,255,255)
        self.tunnelBColour = (200,200,200)
        self.direction = None
        
        self.tunnelActive = False
        self.canShootTunnels = False
        
        
    def destoryTunnels(self):
        self.tunnelAPlaced = False
        self.tunnelBPlaced = False
        self.tunnelALoc = None
        self.tunnelBLoc = None
        
        self.tunnelActive = False
        
    def destoryTunnel(self, tunnelCode): # destory tunnels
        if tunnelCode == "A":
            self.tunnelAPlaced = False
            self.tunnelALoc = None
        
            self.tunnelActive = False
        elif tunnelCode == "B":
            self.tunnelBPlaced = False
            self.tunnelBLoc = None
        
            self.tunnelActive = False
        
    def canTunnel(self, player): # check collisions n if both are active
        if self.tunnelActive:
            
            if self.tunnelAPlaced and player.rectangle.colliderect(self.tunnelARect):
                xB,yB = self.tunnelBLoc
                if self.player.Facing == "Left":
                    xB -= threshold
                elif self.player.Facing == "Right":
                    xB += threshold
                player.tunnelPlayer(xB, yB)
            
            if self.tunnelBPlaced and player.rectangle.colliderect(self.tunnelBRect):
                xA,yA = self.tunnelALoc
                if self.player.Facing == "Left":
                    xA -= threshold
                elif self.player.Facing == "Right":
                    xA += threshold
                player.tunnelPlayer(xA, yA)

        
    def drawTunnels(self): # draw on tunnels
        if self.tunnelActive:
            if self.tunnelAPlaced:
                xA,yA = self.tunnelALoc
                self.tunnelARect = pygame.Rect(xA - 10, yA - 30, 20, 60)
                pygame.draw.rect(self.screen, self.tunnelAColour, pygame.Rect(xA, yA - 20, 20, 60))
                
            if self.tunnelBPlaced:
                xB,yB = self.tunnelBLoc
                self.tunnelBRect = pygame.Rect(xB - 10, yB - 30, 20, 60)
                pygame.draw.rect(self.screen, self.tunnelBColour, pygame.Rect(xB, yB - 20, 20, 60))
        
    def enableTunnelShooting(self):
        self.canShootTunnels = True
        
    def disableTunnelShooting(self):
        self.canShootTunnels = False
        
    def setTunnelDirection(self):        
        if self.player.Facing == "Left":
            self.direction = -0.002
        elif self.player.Facing == "Right":
            self.direction = 0.002

    def movePellet(self):
        self.x = self.player.rectangle.x
        while not self.hitWall:
            #print(self.hitWall)
            self.x += self.direction 
            self.energyPellet = pygame.draw.circle(self.screen, self.tunnelAColour, (self.x, self.player.rectangle.y), 7)
            rect = pygame.Rect(self.energyPellet.left, self.energyPellet.top, self.energyPellet.width, self.energyPellet.height)
            for collidables in self.collisions:
                if rect.colliderect(collidables):
                    print('hit wall')
                    print(f'({self.energyPellet.x}, {self.energyPellet.y})')
                    self.hitWall = True
                    break
        
        if self.currentTunnel == "A":
            self.tunnelALoc = (self.energyPellet.x, self.energyPellet.y)
            self.tunnelAPlaced = True
        elif self.currentTunnel == "B":
            self.tunnelBLoc = (self.energyPellet.x, self.energyPellet.y)
            self.tunnelBPlaced = True
            
        self.tunnelActive = True
        self.drawTunnels()
        self.currentTunnel = None
        
    def shootTunnel(self, tunnelCode, collisions): # what ever way they are facing fire a tunnel to the closest wall till a collision
        # display a fire like animation and then run place 
        print(tunnelCode)
        self.debounce = False
        if not self.debounce:
            if self.canShootTunnels:
                self.debounce = True
                self.currentTunnel = tunnelCode
                self.setTunnelDirection()
                self.collisions = collisions
                self.energyPellet = pygame.draw.circle(self.screen, self.tunnelAColour, (self.player.rectangle.x, self.player.rectangle.y), 7)

                self.hitWall = False
                Thread(target=self.movePellet).start() 
            
