import pygame
import random
import os

pygame.init()
size = width, height = 800, 500
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
FPS = 50


main_window_sprite = pygame.sprite.Group()
picture_for_start = pygame.sprite.Group()
now_sprite = picture_for_start
all_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class StartGame(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('start_game.png', color_key=-1), (50, 50))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = StartGame.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 375, 325

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            from Map_Draw import start_game
            start_game(1, 'm')