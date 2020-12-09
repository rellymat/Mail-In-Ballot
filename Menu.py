from Layer import *


class Cursor(Render):
    def __init__(self, img, buttons):
        self.img = pygame.image.load(img).convert_alpha()
        self.location = buttons[0].location - Vector2(50, -30)
        self.buttons = buttons
        self.sounds = Sound()
        self.point_to = 0

    def move(self, direction):
        self.sounds.play('menu')
        if direction == 'down':
            self.point_to += 1
            if self.point_to == 4:
                self.point_to = 0

        elif direction == 'up':
            self.point_to -= 1
            if self.point_to == -1:
                self.point_to = 3

        else:
            if self.point_to == 1:
                self.buttons[1].change(direction)

        self.change()

    def change(self):
        if self.point_to == 1:
            self.buttons[1].arrow_on = True
        else:
            self.buttons[1].arrow_on = False
        self.location = self.buttons[self.point_to].location - Vector2(50, -30)


class Menu:
    def __init__(self, level):
        self.buttons = [Button('pictures/buttons.png', (400, 100), 'Start'),
                        SelectButton('pictures/buttons.png', (400, 225),self.find_level(level), 'Level'),
                        Button('pictures/buttons.png', (400, 350), 'Manual'),
                        Button('pictures/buttons.png', (400, 475), 'Exit')]
        self.cursor = Cursor('pictures/arrow.png', self.buttons)
        self.blink = 60
        self.manual = False
        self.exit = False

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.exit = True
                return False
            if event.type == pygame.KEYDOWN:
                if not self.manual:
                    if event.key == pygame.K_SPACE:
                        if self.cursor.point_to == 0:
                            return False
                        if self.cursor.point_to == 2:
                            self.manual = True
                        if self.cursor.point_to == 3:
                            pygame.quit()
                            self.exit = True
                            return False
                    if event.key == pygame.K_DOWN:
                        self.cursor.move('down')
                    if event.key == pygame.K_UP:
                        self.cursor.move('up')
                    if event.key == pygame.K_LEFT:
                        self.cursor.move('left')
                    if event.key == pygame.K_RIGHT:
                        self.cursor.move('right')
                if event.key == pygame.K_ESCAPE:
                    self.manual = False
        return True

    def level(self):
        if self.buttons[1].level == 'Easy':
            return 150
        if self.buttons[1].level == 'Medium':
            return 100
        return 75

    def find_level(self, level):
        if level == 150:
            return 'Easy'
        if level == 100:
            return 'Medium'
        return 'Hard'

    def render(self, surface):
        text = create_text('Move with arrow keys and Press space to select','shrikhand', 30, white)
        if self.blink == 60:
            self.blink = 0
        elif 30 <= self.blink < 60:
            self.blink += 1
        elif self.blink < 30:
            surface.blit(text, (250, 600))
            self.blink += 1
        for b in self.buttons:
            b.render(surface)
        self.cursor.render(surface)
        if self.manual:
            Manual().render(surface)


class Manual:
    def __init__(self):
        self.line1 = create_text("Goal:   To reach 270 electoral votes before you're out of the electoral votes or out of lives."
                                 ,'shrikhand', 20, black)
        self.line2 = create_text('How to win:   Move with the arrows keys (up and down) to collect electoral votes (the blue circle)'
                                 , 'shrikhand', 20, black)
        self.line3 = create_text('and shoot the mail ballot at the enemy to prevent him from getting into the White House by pressing the Space key. '
                                 , 'shrikhand', 20, black)

    def render(self, surface):
        pygame.draw.rect(surface, white, pygame.Rect(90, 200, 1250, 200))
        surface.blit(self.line1, (100, 210))
        surface.blit(self.line2, (100, 280))
        surface.blit(self.line3, (100, 310))
        exit = create_text('To back to menu press Escape key'
                            , 'shrikhand', 20, red)
        surface.blit(exit, (110, 370))