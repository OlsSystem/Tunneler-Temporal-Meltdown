# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class ToggleSwitch():
    def __init__(self, x, y, w, h, font_size, screen, text, default=False):
      
        # Requested variables from when creating a new instance of this class.
        self.screen = screen
        self.rect = pygame.Rect(x,y,w,h)
      
        self.font = pygame.font.Font(None, font_size) # Sets the font of the Text
        self.state = default # what the radio menu should show as selected first.
        self.text = text
        
        self.sliderRadius = h // 2 - 3
        

    def draw(self):
        background = (0,180,0) if self.state else (120,120,120)
        pygame.draw.rect(self.screen, background, self.rect, border_radius=self.rect.height // 2)
        
        sliderX = self.rect.x  + (self.rect.width - self.rect.height) if self.state else self.rect.x
        sliderCenter = (sliderX + self.rect.height // 2, self.rect.centery)
        
        pygame.draw.circle(self.screen, (255,255,255), sliderCenter, self.sliderRadius)
        
        if self.text:
            text = self.font.render(self.text, True, (255,255,255))
            self.screen.blit(text, (self.rect.x - text.get_width() - 10, self.rect.y))
        
    def isClicked(self, pos):
        if self.rect.collidepoint(pos):
            self.state = not self.state
            return self.fetchState()
        
        return False
    
    def fetchState(self):
        return self.state