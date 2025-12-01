# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Player:
    def __init__(self, screen, characterImage, scale):
        self.screen = screen
        self.playerCharacter = characterImage
        self.x = 300
        self.y = 300
        self.x_direction = 0
        self.y_direction = 0
        
        self.width = characterImage.get_width()
        self.height = characterImage.get_height()
        
        self.image = pygame.transform.scale(characterImage, (int(self.width * scale), int(self.height * scale))) # Scales down the image using the scale requested
        
        self.speed = 0.1
    
    def draw(self):
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

    def movePlayer(self):
        self.x += self.speed * self.x_direction
        self.y += self.speed * self.y_direction
    