# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Player:
    def __init__(self, screen, characterImage, scale):
        self.screen = screen
        self.playerCharacter = characterImage
        self.x = 220
        self.y = 320
        self.x_direction = 0
        self.y_direction = 0
        
        self.x_last = None
        self.y_last = None
        
        self.width = characterImage.get_width()
        self.height = characterImage.get_height()
        
        self.image = pygame.transform.scale(characterImage, (int(self.width * scale), int(self.height * scale))) # Scales down the image using the scale requested
        
        self.speed = 1
        self.scale = scale
        self.rectangle = pygame.Rect(self.x, self.y, 64, 64)    
        
    def draw(self):
        self.rectangle = pygame.Rect(self.x, self.y, 64, 64)    
        pygame.draw.rect(self.screen, (255,102,255), self.rectangle, 2)
        self.screen.blit(self.image, (self.x, self.y)) # On call draws on the text.
    
    def keyDown(self, event):
        if event.key == pygame.K_LEFT:
            self.x_direction = -1
        elif event.key == pygame.K_RIGHT:
            self.x_direction = 1

    def keyUp(self, event):
        if event.key == pygame.K_LEFT:
            self.x_direction = 0
        elif event.key == pygame.K_RIGHT:
            self.x_direction = 0
                
                
    def movePlayer(self, canCollide=None):
        hasCollided = False
        if canCollide:
            for object in canCollide:
                if object.collidepoint(self.rectangle.topleft) and self.x_direction == 1:
                    break
                    
                if object.collidepoint(self.rectangle.topright) and self.x_direction == -1:
                    break
                    
                if self.rectangle.colliderect(object):
                    hasCollided = True
                    
                    if self.x_direction != 0:
                        self.x_direction = 0
                    if self.y_direction != 0:
                        self.y_direction = 0
                    break
        
        if not hasCollided:
            print(self.speed * self.x_direction)
            self.x += self.speed * self.x_direction
            self.y += self.speed * self.y_direction
            
            
        self.draw()
    