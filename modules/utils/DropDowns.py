# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class DropdownSelect():
    def __init__(self, x, y, w, h, font_size, screen, options, default=None):
      
        # Requested variables from when creating a new instance of this class.
        self.screen = screen
      
        self.font = pygame.font.Font(None, font_size) # Sets the font of the Text
        self.rect = pygame.Rect(x,y,w,h) # Creates a rect based on the given values
        self.options = options 
        self.selected = default or options[0] # what the drop down should display before any interaction
        self.open = False # sets the dropdown to closed.
        
        self.optionsRect = [pygame.Rect(x, y + (i + 1) * h,w,h) for i in range(len(self.options))] # creates rectangles for the options before hand

    def draw(self):
        # Main box
        pygame.draw.rect(self.screen, (50, 50, 50), self.rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.rect, 2)

        # renders the text onto the closed state
        text = self.font.render(self.selected, True, (255, 255, 255))
        self.screen.blit(text, (self.rect.x + 5, self.rect.y + 5))

        # Dropdown options
        if self.open:
            for rect, option in zip(self.optionsRect, self.options): # loops through each option in the options rect and options
                # draws on the boxes below the main one.
                pygame.draw.rect(self.screen, (70, 70, 70), rect) 
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

                # draws on the text for the options
                optionText = self.font.render(option, True, (255, 255, 255))
                self.screen.blit(optionText, (rect.x + 5, rect.y + 5))
        
    def isClicked(self, pos):
        # checks if user has clicked onto the dropdown box
        if self.rect.collidepoint(pos):
            self.open = not self.open # sets the state 
            return False

        if self.open: # checks if open
            for rect, option in zip(self.optionsRect, self.options): # loops through all options and their rects
                if rect.collidepoint(pos): # checks if the person has clicked onto a new box.
                    self.open = False
                    self.selected = option
                    return option

            # Clicked outside
            self.open = False
            return False

        return False