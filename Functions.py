import pygame
import os
import sys
import PIL
from Mario_Map import *

pygame.init()


def collidepoint_by_mask(sprite, group_sprite):
    new = []
    for sp in group_sprite:
        if pygame.sprite.collide_mask(sprite, sp):
            new.append(sp)
    return new


def get_nearest_block(sprite, speed_x, size_block):
    q1 = (sprite.rect.x - 5 * speed_x + get_offset(sprite.image)[2])
    q2 = (sprite.rect.x - 5 * speed_x + sprite.width - get_offset(sprite.image)[3])
    x1 = q1 // size_block
    if q2 % size_block == 0:
        x2 = q2 // size_block
    else:
        x2 = q2 // size_block + 1

    z = sprite.rect.y + sprite.rect.height - get_offset(sprite.image)[1] - 34
    if z % size_block != 0:
        y = z // size_block + 1
    else:
        y = z // size_block
    mapp = World1_1.map
    new = []
    for i in range(x1, x2 + 1):
        for j in range(y, len(mapp)):
            if mapp[j][i] in [3, 4, 9]:
                new.append((j, i))
    if len(new) != 0:
        mini = sorted(new)[0][0]
        return mini * size_block - z   #расстояние до ближайшего блока при падении
    return None  #все свободно


def down_or_side_collidepoint(sprite1, sprite2): #первый сверху, второй снизу или первый левее, второй правее
    if pygame.sprite.collide_mask(sprite1, sprite2):
        if sprite1.rect.y + sprite1.rect.height - get_offset(sprite1.image)[1] - 1 > sprite2.rect.y - get_offset(sprite2.image)[0]:
            return 'UP'
        if sprite1.rect.x + sprite1.rect.width - get_offset(sprite1.image)[3] - 1 < sprite2.rect.x - get_offset(sprite2.image)[2]:
            return 'LEFT'


def find_length(sprite1, sprite2):
        return [sprite1.rect.x + sprite1.rect.width - get_offset(sprite1.image)[3] - (sprite2.rect.x - get_offset(sprite2.image)[2]),
                (sprite1.rect.y + sprite1.rect.height - get_offset(sprite1.image)[1]) - (sprite2.rect.y - get_offset(sprite2.image)[0])]
        #список из 2 значений - по оси х и у. отрицательное - объукт 1 левее объекта 2.  отрицательное - объект 1 сверху, объекта 2





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
    return up - 1, image.get_height() - down - 1, left - 1, image.get_width() - right - 1


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