# ---- Python Modules ---- #
import pygame
import random
# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 
dustParticles = []


class Particle:
    def __init__(self,pos,colour,direction=None,radius=7):
        self.x, self.y = pos
        if direction == "Left":
            self.vy, self.vx = random.randint(-2,2), random.randint(0,10)*.1
            self.x += 20
        elif direction == "Right":
            self.vy, self.vx = random.randint(-2,2), random.randint(-10,0)*.1
        else:
            self.vx, self.vy = random.randint(-2,2), random.randint(-10,0)*.1
        self.rad = radius
        self.colour = colour

    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.rad)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if random.randint(0,100) < 40:
            self.rad -= 1


class Dust:
    def __init__(self,pos,colour,direction=None,radius=7):
        self.pos = pos
        self.particles = []
        for i in range(50):
            self.particles.append(Particle(pos,colour,direction,radius))

    def draw(self,win):
        for i in self.particles:
            i.draw(win)

    def update(self):
        for i in self.particles:
            i.update()
            if i.rad <= 0:
                self.particles.remove(i)
                
def RunParticles(screen):    
    for dust in dustParticles:
        dust.draw(screen)
        dust.update()
    