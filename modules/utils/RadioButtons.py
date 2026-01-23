# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class RadioButtons():
    def __init__(self, x, y, font_size, screen, options, selected=0, spacing=30):
      
        # Requested variables from when creating a new instance of this class.
        self.screen = screen
      
        self.font = pygame.font.Font(None, font_size) # Sets the font of the Text
        self.options = options 
        self.selected = selected # what the radio menu should show as selected first.
        self.radius = 8
        
        self.items = []

        for i, option in enumerate(options):
            yPos = y + i * spacing
            radioPos = (x, yPos)
            textRect = self.font.render(option, True, (255,255,255)).get_rect(midleft=(x + 20, yPos))
            self.items.append((radioPos, textRect, option))

    def draw(self):
        for i, (radioPos, textRect, option) in enumerate(self.items):
            
            if i == self.selected:
                pygame.draw.circle(self.screen, (200,200,200), radioPos, self.radius - 3)
                
            text = self.font.render(option, True, (255,255,255))
            self.screen.blit(text, textRect)
        
    def isClicked(self, pos):
        for i, (radioPos, textRect, _) in enumerate(self.items):
            radioRect = pygame.Rect(
                radioPos[0] - self.radius,
                radioPos[1] - self.radius,
                self.radius * 2,
                self.radius * 2
            )
            
            if radioRect.collidepoint(pos) or textRect.collidepoint(pos):
                self.selected = i
                return self.fetchSelected()
            
        return False
    
    def fetchSelected(self):
        return self.options[self.selected]