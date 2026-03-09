import pygame
import time

class TextBox:
    def __init__(self, x, y, width, height, font_size, screen, placeholder="", text_color=(255,255,255), placeholder_color=(150,150,150)):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)

        self.font = pygame.font.Font(None, font_size)

        self.text = ""
        self.placeholder = placeholder
        self.text_color = text_color
        self.placeholder_color = placeholder_color

        self.active = False
        self.cursor_visible = True
        self.cursor_timer = time.time()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                pass  
            else:
                self.text += event.unicode

    def update(self):
        if time.time() - self.cursor_timer > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = time.time()

    def draw(self):
        pygame.draw.rect(self.screen, (50, 50, 50), self.rect, border_radius=6)
        pygame.draw.rect(self.screen, (200, 200, 200), self.rect, 2, border_radius=6)

        if self.text == "" and not self.active:
            render = self.font.render(self.placeholder, True, self.placeholder_color)
        else:
            render = self.font.render(self.text, True, self.text_color)

        self.screen.blit(render, (self.rect.x + 8, self.rect.y + 8))

        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 8 + render.get_width() + 2
            cursor_y = self.rect.y + 8
            cursor_h = render.get_height()
            pygame.draw.line(self.screen, self.text_color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_h), 2)

    def get_value(self):
        return self.text