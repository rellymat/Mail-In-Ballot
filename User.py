import copy
import os

from Menu import *

os.environ['SDL_VIDEO_CENTERED'] = '1'


class User:
    def __init__(self):
        pygame.init()
        self.level = 150
        self.worldSize = Vector2(1350, 700)
        self.window = pygame.display.set_mode((int(self.worldSize.x), int(self.worldSize.y)))
        pygame.display.set_caption("Mail In Ballot")
        pygame.display.set_icon(pygame.image.load("pictures/mail.png"))
        self.layers = [Background("pictures/grass_template2.jpg", Vector2(0, 0)),
                       WhiteHouse("pictures/white-house.png", Vector2(1100, 250)),
                       Wall("pictures/wall.png", Vector2(1075, 0)),
                       Wall("pictures/wall.png", Vector2(1075, 150)),
                       Wall("pictures/wall.png", Vector2(1075, 300)),
                       Wall("pictures/wall.png", Vector2(1075, 450)),
                       Wall("pictures/wall.png", Vector2(1075, 600))]
        self.player = Player("pictures/donkey.png", Vector2(975, 200), self.worldSize.y - 100)
        self.enemies = []
        self.mails = []
        self.lives = [Life("pictures/heart.png", (5, 2)), Life("pictures/heart.png", (70, 2)), Life("pictures/heart.png", (135, 2))]
        self.clock = pygame.time.Clock()
        self.state = State()
        self.sound = Sound()

    def render(self):
        self.window.fill((0, 0, 0))
        for layer in self.layers:
            layer.render(self.window)
        self.player.render(self.window)
        for enemy in self.enemies:
            enemy.render(self.window)
        for mail in self.mails:
            mail.render(self.window)
        self.state.render(self.window)
        for life in self.lives:
            life.render(self.window)

    def update(self):
        for mail in self.mails:
            if not mail.move():
                self.mails.remove(mail)
        for enemy in self.enemies:
            if not enemy.move():
                del self.lives[0]
                self.enemies.remove(enemy)
        self.state.move()
        self.destroy()

    def destroy(self):
        for mail in self.mails:
            for enemy in self.enemies:
                if enemy.isCollision(mail):
                    self.enemies.remove(enemy)
                    self.mails.remove(mail)
        self.state.isCollision(self.player)

    def randomEnemy(self):
        loc = Vector2(0, random.randint(50, 570))
        enemies = ["fake_news", "election", "count"]
        enemy = random.choice(enemies)
        if enemy == "fake_news":
            self.enemies.append(FakeNews("pictures/fake_news.png", loc))
        if enemy == "election":
            self.enemies.append(Tweet("pictures/election.png", loc))
        if enemy == "count":
            self.enemies.append(Tweet("pictures/count.png", loc))

    def randomState(self):
        loc1 = Vector2(0, random.randint(77, 650))
        self.state.randomChoice(loc1)

    def game_over(self):
        font = pygame.font.SysFont('shrikhand', 64)
        scroll = pygame.image.load('pictures/scroll.png')
        electors = self.state.electorsGet
        blink = 10
        if electors >= 270:
            self.sound.play('athem')
        else:
            self.sound.play('drum')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                        pygame.mixer.pause()
                        self.start_menu(self.level)
            self.render()
            self.window.blit(scroll, (300, 50))
            if electors < 270:
                e = font.render("You Lost", True, red)
                make_america = pygame.image.load('pictures/make_america.png')
                self.window.blit(make_america, (490, 290))
            else:
                e = font.render("You Win", True, blue)
                flag = pygame.image.load('pictures/flag.jpg')
                self.window.blit(flag, (460, 290))
            press = font.render("Press Space to return the menu", True, white)
            self.window.blit(e, (450, 200))
            if blink == 40:
                blink = 0
            elif 20 <= blink < 40:
                blink += 1
            elif blink < 20:
                self.window.blit(press, (150, 600))
                blink += 1
            pygame.display.update()
            self.clock.tick(80)

    def start_menu(self, level=150):
        menu = Menu(level)
        running = True
        while running:
            if not menu.run():
                break
            self.render()
            menu.render(self.window)
            pygame.display.update()
            self.clock.tick(80)
        self.run(menu.level(), menu.exit)

    def reset(self):
        self.enemies.clear()
        self.mails.clear()
        self.state = State()
        i = 5
        while len(self.lives) < 3:
            self.lives.append(Life("pictures/heart.png", (i, 2)))
            i += 65

    def run(self, level, exit):
        if exit:
            return
        running = True
        y = self.player.location.y
        timeEnemy = level
        self.level = level
        cnt_enemy = copy.copy(level)
        delay = 40
        while running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                y -= 3
                y = self.player.setY(y)
            if keys[pygame.K_DOWN]:
                y += 3
                y = self.player.setY(y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if delay == 40:
                            loc = copy.copy(self.player.location)
                            self.mails.append(Mail("pictures/mail.png", loc))
                            delay = 0
                    if event.key == pygame.K_ESCAPE:
                        self.reset()
                        self.start_menu(self.level)
            if timeEnemy == cnt_enemy:
                self.randomEnemy()
                cnt_enemy = 0
            else:
                cnt_enemy += 1

            self.randomState()

            if delay < 40:
                delay += 1

            if not self.lives or self.state.electors == 0:
                self.game_over()
            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(80)
