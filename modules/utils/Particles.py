# ---- Python Modules ---- #
import pygame
import random
# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 
dustParticles = []

class Particle:
    def __init__(self,pos,colour,direction=None,radius=7):
        self.x, self.y = pos # get the position of the particles
        
        # changes the x and y depending on the direction the players facing. otherwise it defaults
        if direction == "Left":
            self.vy, self.vx = random.randint(-2,2), random.randint(0,10)*.1
            self.x += 20
        elif direction == "Right":
            self.vy, self.vx = random.randint(-2,2), random.randint(-10,0)*.1
        else:
            self.vx, self.vy = random.randint(-2,2), random.randint(-10,0)*.1
            
        # sets values that are required for the partciles to be used.
        self.rad = radius
        self.colour = colour

    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.rad) # draws on the particles

    def update(self):
        # updates the x and y
        self.x += self.vx 
        self.y += self.vy
        
        # changes the radius each update for radomness
        if random.randint(0,100) < 40:
            self.rad -= 1


class Dust:
    def __init__(self,pos,colour,direction=None,radius=7):
        self.pos = pos
        self.particles = []
        for i in range(50): # appends 50 lots of particles into a list
            self.particles.append(Particle(pos,colour,direction,radius))

    def draw(self,win):
        for i in self.particles: # draws on the particles.
            i.draw(win)

    def update(self):
        # updates the particles and if the radius is smaller then 0 it removes it from the list
        for i in self.particles: 
            i.update()
            if i.rad <= 0:
                self.particles.remove(i)
                
def RunParticles(screen):    
    for dust in dustParticles: # for all the dust particles draw and update them on the screen
        dust.draw(screen)
        dust.update()