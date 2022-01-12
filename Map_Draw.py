import pygame
import os
from Functions import *
from Background_sprites import *
from Mario_Map import *
from Heros_sprite import *


pygame.init()
size = width, height = 800, 450
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 20

all_sprites = pygame.sprite.Group()
first = pygame.sprite.Group()
second = pygame.sprite.Group()
notouch = pygame.sprite.Group()
touch_but_nomove = pygame.sprite.Group()
player = pygame.sprite.Group()
play = pygame.sprite.Group()
power = pygame.sprite.Group()
touch_down_for_enemy = pygame.sprite.Group()
touch_side_for_enemy = pygame.sprite.Group()
ground = pygame.sprite.Group()



def generate_level(level, bonus):
    sp = [None, Cloud, Big_Cloud, Brick, Ground, Bush, Big_Bush, Hill, Big_Hill, Bonus, Tube_Small, Tube_Sr, Tube_Big,
          Block, Castle, Flag_stick, Turtle_Green, Mushrooms, 'Money', 'Power', Mario, Luigi]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in [1, 2, 5, 6, 7, 8, 14]:
                sp[level[y][x]](x, y, all_sprites, notouch, first)
            elif level[y][x] in [10, 11, 12, 13, 15]:
                sp[level[y][x]](x, y, all_sprites, touch_but_nomove, first)
            elif level[y][x] == 9 and ((x != 0 and level[y][x - 1] == 0) or (x != len(level[y]) - 1 and level[y][x + 1] == 0)):
                sp[level[y][x]](x, y, bonus.pop(0), all_sprites, play, ground, touch_but_nomove, first)
            elif level[y][x] == 9:
                sp[level[y][x]](x, y, bonus.pop(0), all_sprites, play, ground, touch_but_nomove, first)
            elif (x != len(level[y]) - 1 and level[y][x] in [3, 4] and level[y][x + 1] == 0) or\
                    (x != 0 and level[y][x - 1] == 0 and level[y][x] in [3, 4]):
                sp[level[y][x]](x, y, all_sprites, ground, first)
            elif level[y][x] in [3, 4]:
                sp[level[y][x]](x, y, all_sprites, ground, first)
            elif level[y][x] in [16, 17]:
                sp[level[y][x]](x, y, [touch_but_nomove, ground], all_sprites, play, second)
            elif level[y][x] in [20, 21]:
                mario = sp[level[y][x]](x, y, all_sprites, player, second)
    return mario


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self):
        self.dx = -32

map = World1_1().map
bonuses = World1_1().bonuses
camera = Camera()
mario = generate_level(map, bonuses)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
            print('KEYDOWN!')
            key = pygame.key.get_pressed()
            #camera.update()
            mario.get_event(key)
            for sprite in all_sprites:
                camera.apply(sprite)
    pygame.display.flip()
    screen.fill((132, 132, 255))
    first.draw(screen)
    second.draw(screen)
    for el in play:
        el.play()
    clock.tick(FPS)
pygame.quit()