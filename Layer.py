from Units import *
from pygame.math import Vector2


def create_text(text, style, size, color):
    font = pygame.font.SysFont(style, size)
    return font.render(text, True, color)


class Layer(Render):
    def __init__(self, img, location):
        self.img = pygame.image.load(img)
        self.location = location


class Background(Layer):
    def __init__(self, img, location):
        super().__init__(img, location)
        self.transform()

    def transform(self):
        self.img = pygame.transform.scale(self.img, (1350, 700))


class WhiteHouse(Layer):
    def __init__(self, img, location):
        super().__init__(img, location)
        self.scale()

    def scale(self):
        self.img = pygame.transform.scale(self.img, (250, 125))


class Wall(Layer):
    def __init__(self, img, location):
        super().__init__(img, location)
        self.scale()

    def scale(self):
        self.img = pygame.transform.scale(self.img, (30, 150))


class Button(Layer):
    def __init__(self, img, location, text):
        super().__init__(img, location)
        self.renderText = create_text(text, 'comicsansms', 40, black)

    def render(self, surface):
        super().render(surface)
        loc = self.location + Vector2(60, 25)
        surface.blit(self.renderText, loc)


class SelectButton(Button):
    def __init__(self, img, location, level='Easy', text='Level'):
        super().__init__(img, location, text)
        self.arrow = pygame.image.load('pictures/blue arrow.png')
        self.font_level = pygame.font.SysFont('segoeuisemibold', 24)
        self.level = level
        self.arrow_on = False

    def change(self, direction):
        if direction == 'left':
            if self.level == 'Easy':
                self.level = 'Hard'
            elif self.level == 'Medium':
                self.level = 'Easy'
            elif self.level == 'Hard':
                self.level = 'Medium'
        if direction == 'right':
            if self.level == 'Easy':
                self.level = 'Medium'
            elif self.level == 'Medium':
                self.level = 'Hard'
            elif self.level == 'Hard':
                self.level = 'Easy'

    def render(self, surface):
        super().render(surface)
        if self.arrow_on:
            loc_right = self.location + Vector2(10, 95)
            loc_left = self.location + Vector2(175, 95)
            right_arrow = pygame.transform.rotate(self.arrow, 180)
            surface.blit(self.arrow, loc_right)
            surface.blit(right_arrow, loc_left)
            loc_level = self.location + Vector2(80, 95)
            render_level = self.font_level.render(self.level, True, blue)
            surface.blit(render_level, loc_level)
