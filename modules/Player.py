# ---- Python Modules ---- #
import pygame

from modules.utils.Spritesheet import SpriteSheet
# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, sheet, scale):
        super().__init__()
        self.screen = screen
        self.spriteSheet = SpriteSheet(sheet)
        self.animationList = []
        self.animationSteps = 2
        self.x = 220
        self.y = 318
        self.x_direction = 0
        self.y_direction = 0
        
        self.isMoving = False
        
        self.speed = 1
        self.scale = scale
        
        self.listAnimations()
        
        self.currentFrame = 0
        self.image = self.animationList[self.currentFrame]
        self.rectangle = self.image.get_rect(topleft=(self.x, self.y))
        
    def listAnimations(self):
        for x in range(self.animationSteps):
            self.animationList.append(self.spriteSheet.getSprite(x, 138, 182, self.scale, (30,50,30)))
        
    def draw(self):
        #pygame.draw.rect(self.screen, (255,2,200), self.rectangle)  
        if self.isMoving:
            for x in range(self.animationSteps):
                self.screen.blit(self.animationList[x], self.rectangle.topleft) # On call draws on the text.
        else:
            self.screen.blit(self.animationList[0], self.rectangle.topleft) # On call draws on the text.
    
    def keyDown(self, event):
        if event.key == pygame.K_LEFT:
            self.x_direction = -2
        elif event.key == pygame.K_RIGHT:
            self.x_direction = 2
            
        self.isMoving = True


    def keyUp(self, event):
        if event.key == pygame.K_LEFT:
            self.x_direction = 0
        elif event.key == pygame.K_RIGHT:
            self.x_direction = 0
            
        self.isMoving = False
                
                
    def movePlayer(self, canCollide=None):
        hasCollided = False
        if canCollide:
            for object in canCollide:
                if object.collidepoint(self.rectangle.topleft) and self.x_direction == 2:
                    break
                    
                if object.collidepoint(self.rectangle.topright) and self.x_direction == -2:
                    break
                    
                if self.rectangle.colliderect(object):
                    hasCollided = True
                    
                    if self.x_direction != 0:
                        self.x_direction = 0
                    if self.y_direction != 0:
                        self.y_direction = 0
                    break
        
        if not hasCollided:
            self.rectangle.x += self.speed * self.x_direction
            self.rectangle.y += self.speed * self.y_direction
            
            
        self.draw()
    