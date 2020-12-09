import pygame, random
white = (255, 255, 255)
blue = (0, 0, 128)
black = (0, 0, 0)
gold = (255, 215, 0)
red = (255, 0, 0)


class Sound:
    def __init__(self):
        self.sounds = ['music/athem.wav', 'music/buzzer.wav', 'music/coin.wav', 'music/failure.wav', 'music/shot.wav', 'music/tweet.wav',
                       'music/explosion.wav', 'music/win.wav', 'music/alarm.wav', 'music/laugh.wav', 'music/drum.wav', 'music/menu.wav']

    def play(self, name):
        matching = [s for s in self.sounds if name in s]
        sound = pygame.mixer.Sound(matching[0])
        pygame.mixer.Sound.play(sound)


class Render:
    def render(self, surface):
        surface.blit(self.img, self.location)


class Item(Render):
    def __init__(self, img, location, border):
        self.img = pygame.image.load(img).convert_alpha()
        self.location = location
        self.border = border
        self.sounds = Sound()
        self.x = self.y = 100

    def scale(self, x=100, y=100):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(self.img, (x, y))
        return self


class Life(Item):
    def __init__(self, img, location, border=1100):
        super().__init__(img, location, border)


class Player(Item):
    def __init__(self, img, location, border):
        super().__init__(img, location, border)
        self.scale()

    def setY(self, y):
        if 0 > y:
            return 0
        if y > self.border:
            return self.border
        self.location.y = y
        return y


class Mail(Item):
    def __init__(self, img, location, border=0):
        super().__init__(img, location, border)
        self.speed = 5
        self.direction = "left"
        if str(type(self)) == "<class 'Units.Mail'>":
            self.scale(30, 30)
            self.sounds.play('shot')

    def move_left(self):
        self.location.x -= self.speed
        if self.location.x <= self.border:
            return False
        return True

    def move_right(self):
        self.location.x += self.speed
        if self.location.x >= self.border:
            return False
        return True

    def move(self):
        if self.direction == "left":
            return self.move_left()
        return self.move_right()


class FakeNews(Mail):
    def __init__(self, img, location, border=1150):
        super().__init__(img, location, border)
        self.direction = "right"
        self.speed = 4
        self.time = 100
        if str(type(self)) == "<class 'Units.FakeNews'>":
            self.scale(100, 100)
            self.sounds.play('laugh')

    def isCollision(self, mail):
        if self.location.x - 50 <= mail.location.x <= self.location.x + 50 \
                and self.location.y - 25 <= mail.location.y <= self.location.y + 100:
            self.sounds.play('explosion')
            return True
        return False

    def move(self):
        flag = super().move()
        if not flag and self.time != 0:
            if self.time == 100:
                sound = pygame.mixer.Sound("music/buzzer.wav")
                pygame.mixer.Sound.play(sound)
            self.img = pygame.image.load("pictures/X.png")
            self.location.x -= self.speed
            self.time -= 1
            return True
        return flag


class State(FakeNews):
    def __init__(self):
        self.states = {
            'AK': 3,
            'AL': 9,
            'AR': 6,
            'AZ': 11,
            'CA': 55,
            'CO': 9,
            'CT': 7,
            'DC': 3,
            'DE': 3,
            'FL': 29,
            'GA': 16,
            'HI': 4,
            'IA': 6,
            'ID': 4,
            'IL': 20,
            'IN': 11,
            'KS': 6,
            'KY': 8,
            'LA': 8,
            'MA': 11,
            'MD': 10,
            'ME': 4,
            'MI': 16,
            'MN': 10,
            'MO': 10,
            'MS': 6,
            'MT': 3,
            'NC': 15,
            'ND': 3,
            'NE': 5,
            'NH': 4,
            'NJ': 14,
            'NM': 5,
            'NV': 6,
            'NY': 29,
            'OH': 18,
            'OK': 7,
            'OR': 7,
            'PA': 20,
            'RI': 4,
            'SC': 9,
            'SD': 3,
            'TN': 11,
            'TX': 38,
            'UT': 6,
            'VA': 13,
            'VT': 3,
            'WA': 12,
            'WI': 10,
            'WV': 5,
            'WY': 3
        }
        self.electors = 538
        self.electorsGet = 0
        self.state, self.x, self.y = None, None, None
        self.isChange, self.soundWin = False, True
        self.speed = 5
        self.border = 1200
        self.time = 100
        self.color = blue
        self.sounds = Sound()
        self.c1, self.c3 = 0, 128
        self.stateFont = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiuibold', 16)
        self.eleFont = pygame.font.SysFont('shrikhand', 32)

    def randomChoice(self, location):
        if self.state is None and len(self.states):
            self.state = random.choice(list(self.states.items()))
            del self.states[self.state[0]]
            self.x, self.y = location

    def render(self, surface):
        if self.x:
            pygame.draw.circle(surface, self.color, (self.x, self.y), 40)
            state_name = self.stateFont.render(self.state[0], True, white)
            state_elector = self.stateFont.render(str(self.state[1]), True, white)
            surface.blit(state_name, (self.x - 12, self.y - 20))
            surface.blit(state_elector, (self.x - 9, self.y - 3))
        if self.electorsGet >= 270:
            if self.soundWin:
                self.sounds.play('win')
                self.soundWin = False
            elector = self.eleFont.render("Won - " + str(self.electorsGet), True, gold)
        else:
            elector = self.eleFont.render("Won - " + str(self.electorsGet), True, white)
        left = self.eleFont.render("Left - " + str(self.electors), True, red)
        title = self.eleFont.render("Electoral votes: ", True, black)
        surface.blit(elector, (550, 3))
        surface.blit(title, (250, 3))
        surface.blit(left, (770, 3))

    def move(self):
        if self.y and self.x < self.border:
            self.x += self.speed
        elif self.x == self.border:
            if self.changeToRed():
                self.sounds.play("failure")
                self.remove(False)
                self.color = blue
                self.isChange = False

    def changeToRed(self):
        if self.c1 != 255:
            self.c1 += 5
        if self.c3 != 0:
            self.c3 -= 2
        self.color = (self.c1, 0, self.c3)
        if self.c1 == 255 and self.c3 == 0:
            self.c1, self.c3 = 0, 128
            return True
        return False

    def isCollision(self, player):

        if self.y:
            if self.x - 80 <= player.location.x <= self.x + 40 \
                    and self.y - 125 <= player.location.y <= self.y + 40:
                self.remove(True)
                self.sounds.play("coin")
                return True
        return False

    def remove(self, flag):
        self.electors -= self.state[1]
        if flag:
            self.electorsGet += self.state[1]
        self.x, self.y, self.state = None, None, None


class Tweet(FakeNews):
    def __init__(self, img, location, border=1150):
        super().__init__(img, location, border)
        self.sounds.play('tweet')
        self.speed = 3

    def isCollision(self, mail):
        if mail.location.x <= self.location.x + 175 \
                and self.location.y - 25 <= mail.location.y <= self.location.y + 50:
            self.sounds.play('explosion')
            return True
        return False

