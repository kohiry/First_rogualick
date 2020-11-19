import pygame
from pygame.sprite import Sprite, collide_rect
from pygame import Surface

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

class Enemy(Sprite):
    def __init__(self, x, y, width=40, height=80):
        Sprite.__init__(self)
        #self.image = load('data/паук/стоит/паук_стоит_направо_1.png')
        self.image = Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.yvel = 0
        self.xvel = 0
        self.phrase = False
        self.side = 1
        self.isdie = False
        self.helth = 10
        self.onGround = False
        self.damage = False

    def AI(self, hero, platforms):
        way = 1100
        if hero.rect.x >= self.rect.x and hero.rect.x > self.rect.x + self.rect.width-50:
            if hero.rect.y + 20 >= self.rect.y and hero.rect.y + 20 > self.rect.y + self.rect.height:
                self.update(False, True, False, True, platforms)
            elif hero.rect.y + 20 <= self.rect.y and hero.rect.y + 20 < self.rect.y:
                self.update(False, True, True, False, platforms)
            else:
                self.update(False, True, False, False, platforms)
        elif hero.rect.x <= self.rect.x and hero.rect.x < self.rect.x:
            if hero.rect.y + 20 >= self.rect.y and hero.rect.y + 20 > self.rect.y + self.rect.height:
                self.update(True, False, False, True, platforms)
            elif hero.rect.y + 20 <= self.rect.y and hero.rect.y + 20 < self.rect.y:
                self.update(True, False, True, False, platforms)
            else:
                self.update(True, False, False, False, platforms)
        else:
            if hero.rect.y + 20 >= self.rect.y and hero.rect.y + 20 > self.rect.y + self.rect.height:
                self.update(False, False, False, True, platforms)
            elif hero.rect.y + 20 <= self.rect.y and hero.rect.y + 20 < self.rect.y:
                self.update(False, False, True, False, platforms)
            else:
                self.update(False, False, False, False, platforms)

    def update(self, left, right, up, down, platforms):
        # лево право
        SPEED = 5
        if not self.isdie:
            if left:
                self.xvel = -SPEED  * 0.5
                self.side = -1
                #self.AnimeEnemyGoLeft.blit(self.image, (0, 0))
            if right:
                self.xvel = SPEED * 0.5
                self.side = 1
                #self.AnimeEnemyGoRight.blit(self.image, (0, 0))
            if not (left or right):
                self.xvel = 0
            if up:
                self.yvel = -SPEED  * 0.5
                #self.AnimeEnemyGoLeft.blit(self.image, (0, 0))
            if down:
                self.yvel = SPEED * 0.5
                #self.AnimeEnemyGoRight.blit(self.image, (0, 0))
            if not (up or down):
                self.yvel = 0
                #if self.side == 1:
                    #self.AnimeEnemyStayRight.blit(self.image, (0, 0))
                #elif self.side == -1:
                    #self.AnimeEnemyStayLeft.blit(self.image, (0, 0))
        #else:
            #if self.side == 1:
                #self.AnimeEnemyDieRight.blit(self.image, (0, 0))
            #elif self.side == -1:
                #self.AnimeEnemyDieLeft.blit(self.image, (0, 0))
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    #def hit(self):
        #choice(self.SPIDER_AUDIO).play()

    def collide(self, xvel, yvel, platforms):
        for pl in platforms:
            if collide_rect(self, pl):
                #self.serf = True
                if yvel > 0:
                    self.onGround = True
                    self.rect.bottom = pl.rect.top
                if yvel < 0:
                    self.yvel = 0
                    self.rect.top = pl.rect.bottom
                if xvel < 0:
                    self.yvel = 0
                    self.rect.left = pl.rect.right
                if xvel > 0:
                    self.yvel = 0
                    self.rect.right = pl.rect.left

    def die(self):
        self.isdie = True  # включу запутанного моба
        self.xvel = 0
        self.yvel = 0

class Ball(Sprite):
    def __init__(self, x, y, side):
        Sprite.__init__(self)
        #self.damage_audio = Sound().DAMAGE_AUDIO
        #set_mode((0, 0), HWSURFACE| DOUBLEBUF| FULLSCREEN)
        #if side == 1:
            #self.image = load('data\\штуки\\выстрел_паутины_R.png').convert_alpha()
        #else:
            #self.image = load('data\\штуки\\выстрел_паутины_L.png').convert_alpha()
        self.image = Surface((10, 10))
        self.rect = self.image.get_rect()
        self.side = side
        self.rect.x = x
        self.rect.y = y
        self.xvel = 0
        self.die = False
        #self.ball =

    def update(self, hero, enemys):
        SPEED = 35
        # лево право
        if self.side == -1:
            self.xvel = -SPEED * 1
        if self.side == 1:
            self.xvel = SPEED * 1

        self.rect.x += self.xvel

class Hero(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load(r'data\heroR.png')
        self.rect = self.image.get_rect()
        self.spawn = '@'
        self.level = 0
        self.side = 1
        self.yvel = 0
        self.xvel = 0
        self.speed = 5
        self.animcount = 0
        self.R = pygame.image.load(r'data\heroR.png')
        self.L = pygame.image.load(r'data\heroL.png')

    def change_coord(self, coord):
        self.rect.x, self.rect.y = coord

    def upd(self, left, right, up, down, platforms):
        if left:
            self.side = -1
            self.xvel = -self.speed
            self.image = self.L
        if right:
            self.side = 1
            self.xvel = self.speed
            self.image = self.R
        if up:
            self.yvel = -self.speed
        if down:
            self.yvel = self.speed
        if not left and not right:
            self.xvel = 0
        if not up and not down:
            self.yvel = 0

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
                if yvel < 0:
                    self.rect.top = pl.rect.bottom
                if xvel < 0:
                    self.rect.left = pl.rect.right
                if xvel > 0:
                    self.rect.right = pl.rect.left
