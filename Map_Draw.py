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
FPS = 30

all_sprites = pygame.sprite.Group()
first = pygame.sprite.Group()
second = pygame.sprite.Group()
notouch = pygame.sprite.Group()
touch_but_nomove = pygame.sprite.Group()
player = pygame.sprite.Group()
play = pygame.sprite.Group()
power = pygame.sprite.Group()
ground = pygame.sprite.Group()
enemy = pygame.sprite.Group()
bonus = pygame.sprite.Group()
brick = pygame.sprite.Group()
ground_block = pygame.sprite.Group()
tube = pygame.sprite.Group()
zero = pygame.sprite.Group()
sp = [None, Cloud, Big_Cloud, Brick, Ground, Bush, Big_Bush, Hill, Big_Hill, Bonus, Tube_Small, Tube_Sr, Tube_Big,
          Block, Castle, None_tube, Turtle_Green, Mushrooms, Money, Mushroom_Power, Mario]


def generate_level(level, bonuss):
    mario = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in [1, 2, 5, 6, 7, 8, 14]:
                sp[level[y][x]](x, y, all_sprites, notouch, first)
            elif level[y][x] in [10, 11, 12]:
                sp[level[y][x]](x, y, all_sprites, ground_block, touch_but_nomove, first)
                level = make_tube(level[y][x], x, y, sp[15], level, all_sprites, ground, brick, ground_block, touch_but_nomove, zero)
            elif level[y][x] == 9 and ((x != 0 and level[y][x - 1] == 0) or (x != len(level[y]) - 1 and level[y][x + 1] == 0)):
                sp[level[y][x]](x, y, bonuss.pop(0), all_sprites, brick, bonus, ground, play, touch_but_nomove, first)
            elif level[y][x] == 9:
                sp[level[y][x]](x, y, bonuss.pop(0), all_sprites, bonus, brick, ground, play, touch_but_nomove, first)
            elif level[y][x] in [3, 4]:
                sp[level[y][x]](x, y, all_sprites, ground, brick, touch_but_nomove, first)
            elif level[y][x] == 13:
                sp[level[y][x]](x, y, all_sprites, ground, brick, ground_block, touch_but_nomove, first)
            elif level[y][x] in [16, 17]:
                sp[level[y][x]](x, y, [ground_block, ground, ground_block], enemy,  all_sprites, play, second)
            elif level[y][x] == 20:
                mario = sp[level[y][x]](x, y, 'm', [enemy, ground, brick, touch_but_nomove, ground_block, tube], all_sprites, player, second)
    return mario


map = World1_1.map
bonuses = World1_1().bonuses
mario = generate_level(map, bonuses)
mario.rect.x = 0

class Camera:
    def __init__(self):
        self.dx = 0
        self.x = 0

    # позиционировать камеру на объекте target
    def update(self, obj):
        print(mario.rect)
        if mario.rect.x > height // 2:
            self.dx = mario.rect.x - (height // 2)
            print(self.dx)
            self.x += self.dx
            for el in obj:
                el.rect.x -= self.dx
camera = Camera()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass
    camera.update(all_sprites)
    key = pygame.key.get_pressed()
    mario.get_event(key, camera.x)
    mario.update()
    for el in play:
        el.play(camera.x)
    pygame.display.flip()
    screen.fill((132, 132, 255))
    bonus.draw(screen)
    zero.draw(screen)
    first.draw(screen)
    second.draw(screen)
    clock.tick(FPS)
pygame.quit()