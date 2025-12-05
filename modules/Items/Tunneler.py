# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Tunneler():
    def __init__(self, screen, tunnelAImg, tunnelBImg, player):
        self.screen = screen
        self.tunnelA = tunnelAImg
        self.tunnelB = tunnelBImg
        self.player = player
        
        self.tunnelAPlaced = False
        self.tunnelBPlaced = False
        self.tunnelALoc = None
        self.tunnelBLoc = None
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
        print('bang')
        
    def drawTunnels(self): # draw on tunnels
        print('bang')
        
    def enableTunnelShooting(self):
        self.canShootTunnels = True
        
    def disableTunnelShooting(self):
        self.canShootTunnels = False
        
    def setTunnelDirection(self):        
        if self.player.Facing == "Left":
            self.direction = -3
        elif self.player.Facing == "Right":
            self.direction = 3
        
    def shootTunnel(self, tunnelCode): # what ever way they are facing fire a tunnel to the closest wall till a collision
        # display a fire like animation and then run place 
        if self.canShootTunnels:
            self.setTunnelDirection()
            
            self.energyPellet = pygame.draw.circle(self.screen, self.tunnelAColour, (self.player.rectangle.x, self.player.rectangle.y), 2)