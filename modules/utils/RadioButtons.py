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
        
        self.items = [] # defins the list of items
        
        # loops through all enumerated options and create a rect of each and add to list
        for i, option in enumerate(options):
            yPos = y + i * spacing
            radioPos = (x, yPos)
            textRect = self.font.render(option, True, (255,255,255)).get_rect(midleft=(x + 20, yPos))
            self.items.append((radioPos, textRect, option))

    def draw(self):
        for i, (radioPos, textRect, option) in enumerate(self.items): # loops through the list
            
            if i == self.selected: # if currently on selected button
                pygame.draw.circle(self.screen, (200,200,200), radioPos, self.radius - 3) # draw on selected cricle
                
            # display texts next to the button
            text = self.font.render(option, True, (255,255,255))
            self.screen.blit(text, textRect)
        
    def isClicked(self, pos):
        # loops through all the radio buttons
        for i, (radioPos, textRect, _) in enumerate(self.items):
            # create a rect for the radio buttons based on the selected one
            radioRect = pygame.Rect(
                radioPos[0] - self.radius,
                radioPos[1] - self.radius,
                self.radius * 2,
                self.radius * 2
            )
            
            # check if the button has been clicked and change the selected if it has
            if radioRect.collidepoint(pos) or textRect.collidepoint(pos):
                self.selected = i
                return self.fetchSelected()
            
        return False
    
    # return the option that is currently selected
    def fetchSelected(self):
        return self.options[self.selected]