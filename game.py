import pygame

from obj import *
import level
pygame.init()


class Game:
    def __init__(self):
        self.running = True
        self.LEFT = False
        self.RIGHT = False
        self.UP = False
        self.DOWN = False
        pygame.display.set_mode((0, 0))
        self.HERO = Hero()
        self.group_platform = pygame.sprite.Group()
        self.group_draw = pygame.sprite.Group()
        self.Enemys = pygame.sprite.Group()
        self.Bullet = pygame.sprite.Group()
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
        for i in self.Enemys:
            i.AI(self.HERO, self.group_platform)
        self.Enemys.draw(self.screen)
        self.damage()
        """
        if not self.click:
            font = pygame.font.Font(r'other\pixle_font.ttf', 22)
            txt = font.render('очень по быстрому запилил), ЛКМ чтобы убрать меня', 1, white)
            self.window.blit(txt, (50, 20))"""
        self.window.blit(self.screen, self.middle)
        pygame.display.flip()

    def damage(self):
        info = pygame.sprite.groupcollide(self.Bullet, self.Enemys, True, False)
        keys_bullet = info.keys()
        pygame.sprite.groupcollide(self.Bullet, self.group_platform, True, False)
        self.Bullet.update(self.HERO, self.Enemys)
        for i in keys_bullet:
            for j in info[i]:
                #self.sound.DAMAGE_AUDIO.play()
                j.helth -= 1
                j.damage = True
                #j.hit()
                if j.helth < 0:
                    j.die()
                break
        self.Bullet.draw(self.screen)

    def game_cycle(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        self.Bullet.add(Ball(self.HERO.rect.x + self.HERO.rect.width // 2, self.HERO.rect.y + self.HERO.rect.height // 2, self.HERO.side))

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.LEFT = True
                    if event.key == pygame.K_d:
                        self.RIGHT = True
                    if event.key == pygame.K_w:
                        self.UP = True
                    if event.key == pygame.K_s:
                        self.DOWN = True

                    if event.key == pygame.K_ESCAPE:
                        self.running = False


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.LEFT = False
                    if event.key == pygame.K_d:
                        self.RIGHT = False
                    if event.key == pygame.K_w:
                        self.UP = False
                    if event.key == pygame.K_s:
                        self.DOWN = False

            self.HERO.upd(self.LEFT, self.RIGHT, self.UP, self.DOWN, self.group_platform)
            self.draw()
            self.clock.tick(60)

    def make_level(self, level):
        x, y = -self.lens, 0
        for row in level:
            for col in row:
                if col == '-':
                    pl = Platform(x, y, self.lens, self.lens)
                    self.group_platform.add(pl)
                    #self.group_draw.add(pl)
                if col == '@':
                    self.HERO.change_coord((x, y))
                if col == '#':
                    self.Enemys.add(Enemy(x, y))

                x += self.lens
            y += self.lens
            x = -self.lens


if __name__ == '__main__':
    game = Game()
    game.make_level(level.level)
    game.game_cycle()
