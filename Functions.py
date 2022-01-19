import pygame
import os
import sys
from Mario_Map import *


pygame.init()


def up_mask(sprite1, sprite2):
    print(sprite1.rect.center[1], sprite2.rect.top)
    if sprite1.rect.center[1] < sprite2.rect.top:
        print('Yes')
    else:
        print('no')


def collidepoint_by_mask(sprite, group_sprite):
    new = []
    for sp in group_sprite:
        if pygame.sprite.collide_mask(sprite, sp):
            new.append(sp)
    return new


def get_nearest_block(sprite, size_block, off):
    q1 = (sprite.rect.x + get_offset(sprite.image)[2] + off)
    q2 = (sprite.rect.x + sprite.image.get_width() - get_offset(sprite.image)[3] + off)
    x1 = (q1 // size_block)
    x2 = (q2 // size_block)
    z = sprite.rect.y + sprite.rect.height - get_offset(sprite.image)[1] - 34
    z1 = sprite.rect.y + get_offset(sprite.image)[0] - 34
    y = z // size_block
    y1 = z1 // size_block
    if z % size_block != 0:
        y += 1
    if z1 % size_block != 0:
        y1 += 1
    mapp = World1_1.map
    new, new_up, new_left, new_right = [], [], [], []
    if y > len(mapp) or x2 < 0:
        return ('kill',)
    if x2 - x1 == 2:
        x2 -= 1
    if y1 == y:
        y1 -= 1
    #print(x1, x2, y1, y)
    for i in range(x1, x2 + 1):
        for j in range(y, len(mapp)):
            if mapp[j][i] in [3, 4, 9, 13, 15]:
                new.append((j, i, mapp[j][i]))
                continue
    for i in range(x1, x2 + 1):
        for j in range(0, y1):
            if mapp[j][i] in [3, 4, 9, 13, 15]:
                new_up.append((j, i, mapp[j][i]))
                continue
    if len(new) != 0:
        mini = sorted(new)[0]
        mini = (mini[0] * size_block - z, mini[-1])   #расстояние до ближайшего блока при падении
    else: mini = None, None  #все свободно
    if len(new_up) != 0:
        mini1 = sorted(new_up)[-1]
        mini1 = ((sprite.rect.y + get_offset(sprite.image)[0]) - (mini1[0] + 1) * size_block - 34, mini1[-1])
    else: mini1 = None, None

    for i in range(y1, y):
        for j in range(0, x1):
            if mapp[i][j] in [3, 4, 9, 13, 15]:
                new_left.append((j, i, mapp[i][j]))
                continue
    if len(new_left) != 0:
        mini2 = sorted(new_left)[-1]
        mini2 = (q1 - (mini2[0] + 1) * size_block, mini2[-1])   #расстояние до ближайшего блока при падении
    else: mini2 = None, None  #все свободно

    for i in range(y1, y):
        for j in range(x2 + 1, len(mapp[0])):
            if mapp[i][j] in [3, 4, 9, 13, 15]:
                new_right.append((j, i, mapp[i][j]))
                continue
    if len(new_right) != 0:
        mini3 = sorted(new_right)[0]
        mini3 = (mini3[0] * size_block - q2, mini3[-1])   #расстояние до ближайшего блока при падении
    else: mini3 = None, None
    #print(sorted(new_left), sorted(new_right))#все свободно
    #print('minis', mini, mini1, mini2, mini3)
    return mini, mini1, mini2, mini3


def make_tube(number, x, y, object, map, *arg):
    map[y][x] = [map[y][x], 15]
    for i in range(2):
        for j in range(number - 8):
            object(x + i, y - j, arg)
            map[y - j][x + i] = 15
    return map

def flip(images):
    for i in range(len(images)):
        images[i] = pygame.transform.flip(images[i], True, False)
    return images


def get_offset(image):
    z = pygame.mask.from_surface(image).outline()
    down = max(map(lambda x: x[1], z))
    up = min(map(lambda x: x[1], z))
    left = min(map(lambda x: x[0], z))
    right = max(map(lambda x: x[0], z))

    return up, image.get_height() - down - 1, left - 1, image.get_width() - right - 1


def cut_sheet(self, sheet, columns, rows, a1, a2, b1, b2):
    self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
    frame = []
    for j in range(b1, b2):
        for i in range(a1, a2):
            frame_location = (self.rect.w * i, self.rect.h * j)
            frame.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
    return frame


def load_image(name, color_key=None, width=None, height=None):
    fullname = os.path.join('data', name)
    try:
        if not color_key:
            image = pygame.image.load(fullname).convert_alpha()
        else:
            image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
            print(color_key)
        image.set_colorkey(color_key)
    if width != None or height != None:
        image = pygame.transform.scale(image, (width, height))
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_music(name):
    fullname = os.path.join("music", name)
    try:
        return pygame.mixer.Sound(fullname)
    except pygame.error as ex:
        print("Cant load music {} because: {}".format(name, ex))


def text(text, color):
    font = pygame.font.Font(None, 30)
    string = font.render(text, 1, color)
    return string