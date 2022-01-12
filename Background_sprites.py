from Functions import *
import pygame
k = 0
screen = pygame.display.set_mode((200, 200))
pygame.init()
class Base(pygame.sprite.Sprite):
    is_collidepoint = False  #материальность для столкновений
    can_i_beat_it = False
    size = width, height = 32, 32
    image = load_image('None.png')
    offset_x, offset_y = 0, 34

    def __init__(self, x, y, *group):
        global k
        try:
            super().__init__(*group)
            self.image = self.image
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (self.width * x + self.offset_x, self.height * (y + 1) + self.offset_y)
        except:
            k += 1
            print(*group)


    def beat_block_1(self):
        pass

    def beat_block_0(self):
        pass

    def beat_block(self, mario_size): #большой(1) или маленький(0) марио
        if mario_size == 1 and self.can_i_beat_it:
            self.beat_block_1()
            self.kill()
        elif mario_size == 0 and self.can_i_beat_it:
            self.beat_block_0()

    def play(self): #мигание
        pass


class Cloud(Base):
    image = load_image('cloud.png')


class Big_Cloud(Base):
    image = load_image('cloud_big.png')


class Brick(Base):
    image = load_image('kirpich33.png', width=33, height=33)
    can_i_beat_it = True
    is_collidepoint = True
    vx = 2 #начальная скорость x
    vy = 0 #начальная скорость y
    g = 2 #ускорение

    def beat_block_1(self):
        image_broken = load_image('kirpich_broken.png')
        #распадается на квадратики
        pass

    def beat_block_0(self):
        #приподнимается и возвращается на место
        pass


class Ground(Base):
    image = load_image('ground.png',width=33, height=33)
    is_collidepoint = True


class Bush(Base):
    image = load_image('bush_small.png', color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(x, y, *group)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (32 * x - 16, 32 * (y + 1) + 34)


class Big_Bush(Bush):
    image = load_image('bush.png')


class Hill(Base):
    image = load_image('hill.png')


class Big_Hill(Base):
    image = load_image('hill_big.png')


class Bonus(Base):
    images = [load_image('bonus.png', width=33, height=33), load_image('bonus2.png', width=33, height=33),
              load_image('bonus3.png', width=33, height=33), load_image('bonus4.png', width=33, height=33)]
    image = images[0]
    is_collidepoint = True

    def __init__(self, x, y, arg, *group): #arg - список всех объектов (монеты, ускорители), выпадающих из куба
        super().__init__(x, y, *group)
        self.arg = arg
        self.timers = [15, 10, 10]
        self.timer = self.timers[0]

    def play(self):
        if len(self.arg) != 0 and self.timer == 0:
            self.image = self.images[(self.images.index(self.image) + 1) % 3]
            self.timer = self.timers[self.images.index(self.image)]
        elif len(self.arg) == 0:
            self.image = self.images[-1]
        self.timer -= 1


class Tube_Small(Base):
    image = load_image('tube3.png')
    is_collidepoint = True


class Tube_Sr(Base):
    image = load_image('tube2.png')
    is_collidepoint = True


class Tube_Big(Base):
    image = load_image('tube1.png')
    is_collidepoint = True


class Block(Base):
    image = load_image('block33.png', width=32, height=32)
    is_collidepoint = True


class Castle(Base):
    image = load_image('castle1.png')


class Flag_stick(Base):
    image = load_image('flag_stick.png')




