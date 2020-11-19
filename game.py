import pygame
from pygame.sprite import Sprite
import level
pygame.init()

class Platform(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self)
        self.name = '-'
        self.image = pygame.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Back(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load(r'data\back.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Hero(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load(r'data\heroR.png')
        self.rect = self.image.get_rect()
        self.spawn = '@'
        self.level = 0
        self.side = 1
        self.gravity = 0.1
        self.onGround = False
        self.yvel = 0
        self.xvel = 0
        self.speed = 5
        self.animcount = 0
        self.R = self.image = pygame.image.load(r'data\heroR.png')
        self.L = self.image = pygame.image.load(r'data\heroL.png')

    def change_coord(self, coord):
        self.rect.x, self.rect.y = coord

    def upd(self, left, right, platforms):
        if left:
            self.xvel = -self.speed
            self.image = self.L
        elif right:
            self.xvel = self.speed
            self.image = self.R
        elif not left and not right:
            self.xvel = 0

        if not self.onGround:
            self.yvel += self.gravity
        else:
            self.yvel = 0

        self.onGround = False
        if self.xvel > 0 or self.xvel < 0:
            self.animcount += 1
            if self.animcount == 15:
                self.animcount = 0
                self.rect.y -= 10
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        pl = pygame.sprite.spritecollideany(self, platforms, collided = None)
        if pl != None:
            if pl.name == '-':
                #self.serf = True
                if yvel > 0:
                    self.rect.bottom = pl.rect.top
                    self.onGround = True
                if yvel < 0:
                    self.rect.top = pl.rect.bottom
                if xvel < 0:
                    self.rect.left = pl.rect.right
                if xvel > 0:
                    self.rect.right = pl.rect.left



class Game:
    def __init__(self):
        self.running = True
        self.LEFT = False
        self.RIGHT = False
        pygame.display.set_mode((0, 0))
        self.HERO = Hero()
        self.group_platform = pygame.sprite.Group()
        self.group_draw = pygame.sprite.Group()
        back = Back(0, 0)
        self.group_draw.add(back)
        self.group_draw.add(self.HERO)
        self.lens = 54
        self.SIZE = self.WIDTH, self.HEIGHT = 600, 600
        self.clock = pygame.time.Clock()
        self.sound = pygame.mixer.Sound(file=r'sound\waterfall.wav')
        self.sound.set_volume(0.2)
        self.sound.play(-1)
        self.click = False

        self.middle = ((1080 - self.WIDTH)//2, (720 - self.HEIGHT)//2)
        self.size = width, height = 1080, 720
        self.window = pygame.display.set_mode(self.size)
        self.screen = pygame.Surface(self.SIZE)
        pygame.display.set_caption('Game.')

    def draw(self):
        white = (255, 255, 255)
        self.screen.fill(white)
        self.window.fill((0, 0, 0))
        self.group_draw.draw(self.screen)
        if not self.click:
            font = pygame.font.Font(r'other\pixle_font.ttf', 22)
            txt = font.render('очень по быстрому запилил), ЛКМ чтобы убрать меня', 1, white)
            self.window.blit(txt, (50, 20))
        self.window.blit(self.screen, self.middle)
        pygame.display.flip()

    def game_cycle(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        self.click = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.LEFT = True
                    if event.key == pygame.K_d:
                        self.RIGHT = True
                    if event.key == pygame.K_ESCAPE:
                        self.running = False


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.LEFT = False
                    if event.key == pygame.K_d:
                        self.RIGHT = False

            self.HERO.upd(self.LEFT, self.RIGHT, self.group_platform)
            print(self.HERO.rect.x)
            self.draw()
            self.clock.tick(60)

    def make_level(self, level):
        x, y = 0, 0
        for row in level:
            for col in row:
                if col == '-':
                    pl = Platform(x, y, self.lens, self.lens)
                    self.group_platform.add(pl)
                    #self.group_draw.add(pl)
                if col == '@':
                    self.HERO.change_coord((x, y))

                x += self.lens
            y += self.lens
            x = 0


if __name__ == '__main__':
    game = Game()
    game.make_level(level.level)
    game.game_cycle()
