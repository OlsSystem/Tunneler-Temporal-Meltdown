# ---- Python Modules ---- #
import pygame

# ---- Misc Variables ---- #


# ---- Initialising Variables ---- #


class Slider:
    def __init__(self, x, y, w, h, font_size, screen, text, min=0, max=100, default=0):

        # Requested variables from when creating a new instance of this class.
        self.screen = screen

        self.x, self.y, self.width = x, y, w

        self.font = pygame.font.Font(None, font_size)  # Sets the font of the Text
        self.sliderRadius = 8
        self.height = h
        self.min = min
        self.max = max
        self.text = text

        self.value = default
        self.dragging = False

        # creates a rect for the main body of the slider
        self.sliderBodyRect = pygame.Rect(x, y, w, h)

        # sets the x and y of the slider depending on default value
        self.sliderX = (self.x + (self.value - self.min) / (self.max - self.min) * self.width)
        self.sliderY = self.y + self.height // 2

        # sets the slider to the current default amount and moves it to the correct position
        percent = (self.value - self.min) / (self.max - self.min)
        self.sliderX = self.x + percent * self.width

    def draw(self):
        textRender = self.font.render(self.text, True, (255, 255, 255)) # renders the label text
        valueRender = self.font.render(f"{int(self.value)}%", True, (200, 200, 200)) # renders the value as percent

        # draws on both the label and value.
        self.screen.blit(textRender, (self.x, self.y - 35))
        self.screen.blit(valueRender, (self.x + self.width - valueRender.get_width(), self.y - 35))

        # draws on the main body of the slider
        pygame.draw.rect(self.screen, (180, 180, 180), self.sliderBodyRect, border_radius=3)

        # draws on how much of the bar is filled depending on value
        filledBarRect = pygame.Rect(self.x, self.y, self.sliderX - self.x, self.height)
        pygame.draw.rect(self.screen, (100, 200, 255), filledBarRect, border_radius=3)

        # draws on the sliders knob
        pygame.draw.circle(self.screen, (255, 255, 255), (int(self.sliderX), self.sliderY), self.sliderRadius)
        pygame.draw.circle(self.screen, (60, 60, 60), (int(self.sliderX), self.sliderY), self.sliderRadius, 2)

        # updates pos
        self.update()

    # sets the position of the slider based on the mouse dragging it
    def setSliderPos(self, pos):
        self.sliderX = max(self.x, min(pos[0], self.x + self.width))
        percent = (self.sliderX - self.x) / self.width
        self.value = self.min + percent * (self.max - self.min)

    # updates the sliders pos based if the knobs being dragged and its location
    def update(self):
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.setSliderPos(mouse_pos)


    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # check if the mouse has been clicked
            dx = event.pos[0] - self.sliderX
            dy = event.pos[1] - self.sliderY

            # checks if the slider is being clicked anywhere on the bar or the knob has been clicked.
            if (self.sliderBodyRect.collidepoint(event.pos) or dx * dx + dy * dy <= self.sliderRadius**2): 
                self.dragging = True # sets dragging to true
                self.setSliderPos(event.pos) # changes sliders position

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # check if the mouse button has been released
            self.dragging = False # set dragging to false

        return self.fetchValue() # return new value

    # fetch value
    def fetchValue(self):
        return self.value
