# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, characterImage, scale):
        super().__init__()
        self.screen = screen
        self.playerCharacter = characterImage
        self.x = 220
        self.y = 318
        self.x_direction = 0
        self.y_direction = 0
        
        self.x_last = None
        self.y_last = None
        
        self.width = characterImage.get_width()
        self.height = characterImage.get_height()
        
        self.player = pygame.transform.scale(characterImage, (int(self.width * scale), int(self.height * scale))) # Scales down the image using the scale requested
        self.rectangle = self.player.get_rect(topleft=(self.x, self.y))
        
        self.speed = 1
        self.scale = scale
        
    def draw(self):
        pygame.draw.rect(self.screen, (255,2,200), self.rectangle)  
        self.screen.blit(self.player, self.rectangle.topleft) # On call draws on the text.
    
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
            self.rectangle.x += self.speed * self.x_direction
            self.rectangle.y += self.speed * self.y_direction
            
            
        self.draw()
    