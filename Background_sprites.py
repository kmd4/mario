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
        super().__init__(*group)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.width * x + self.offset_x, self.height * (y + 1) + self.offset_y)


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
        self.timers = [5, 3, 3]
        self.timer = self.timers[0]

    def play(self, offset):
        if len(self.arg) != 0 and self.timer == 0:
            self.image = self.images[(self.images.index(self.image) + 1) % 3]
            self.timer = self.timers[self.images.index(self.image)]
        self.timer -= 1


    def push(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if len(self.arg) == 1:
                self.image = self.images[-1]
            new_object = self.arg.pop(0)
            return new_object, self.rect.midtop #number of new_object



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


class None_tube(Base):
    image = load_image('None_tube.png', width=32, height=32)

class Button(pygame.sprite.Sprite):
    image = load_image('None_tube.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def clicked(self):
        pass

class Pause(Button):
    flag_not_paused = True
    image = load_image('7.png', color_key=-1, width=50, height=50)


    def clicked(self):
        t = get_paused(self.flag_not_paused)
        self.flag_not_paused = not self.flag_not_paused
        return t

class In_Menu(Button):
    image = load_image('1.png', color_key=-1, width=50, height=50)


class Again(Button):
    image = load_image('16.png', color_key=-1, width=50, height=50)


