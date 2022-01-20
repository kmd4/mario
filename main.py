import pygame
from Map_Draw2 import *
from start_sprite import *
from Functions import *
points = 0


pygame.init()
ARIAL_50 = pygame.font.SysFont('arial', 25)
clock = pygame.time.Clock()
FPS = 50
Hero = 'm'
heros_sprites = pygame.sprite.Group()
start_window_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def data_result(points, coins):
    with  open('data/result.txt', 'r', encoding='utf-8') as f1, open('data/result.txt', 'w', encoding='utf-8') as f2:
        result = f1.readline()
        points_f, coins_f = result.split()[0].split(':')[1], result.split()[1].split(':')[1]
        points = max(points_f, points)
        coins = max(coins_f, coins)
        f2.write(f"points:{points} coins:{coins}")


def start():
    print(1)
    global start_window_sprites
    size = width, height = 800, 450
    screen = pygame.display.set_mode(size)
    image = load_image('fon23.png')
    image_rect = image.get_rect()
    image_rect.center = (width // 2, height // 2)
    screen.blit(image, image_rect)
    start_window_sprites = pygame.sprite.Group()
    pygame.display.set_caption('Mario Bros')
    pygame.display.set_icon(load_image('mar_icon.png'))
    menu = OpenMenu(start_window_sprites)
    start_game = StartGame(start_window_sprites)
    screen.blit(load_image('sky.png'), (0, 0))
    start_window_sprites.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_window_sprites.update(event)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


class MarioChose(pygame.sprite.Sprite):
    image = load_image('mmario.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = MarioChose.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 150, 50

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            global Hero
            Hero = 'm'


class LuidziChose(pygame.sprite.Sprite):
    image = load_image('lluidzi.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = LuidziChose.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 50

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            global Hero
            Hero = 'l'






class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._option_surfaces.append(pygame.font.SysFont('arial', 40).render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

class NextLevel: # окно - меню после завершения первого уровня
    def __init__(self):
        screen.blit(load_image('sky.png'), (0, 0))
        menu = Menu()
        menu.append_option('Пройти еще раз', start_game_world1())
        menu.append_option('Следущий уровень', start_game_world2())
        menu.append_option('Вернуться в меню', start())
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        start()
                    if event.key == 119:
                        menu.switch(-1)
                    if event.key == 115:
                        menu.switch(1)
                    if event.key == 13:
                        menu.select()

            screen.blit(load_image('sky.png'), (0, 0))
            menu.draw(screen, 300, 100, 40)
            pygame.display.flip()





class OpenMenu(pygame.sprite.Sprite):
    image_menu = load_image('8.png', width=50, height=50)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = OpenMenu.image_menu
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 10, 10

    def record(self):
        sky_image = load_image('sky.png')
        screen.blit(sky_image, (0, 0))
        pygame.display.set_caption('Достижения')
        #pygame.display.set_icon(pygame.image.load('data/mar_icon.png'))

    def rules(self):
        pygame.display.set_caption('Правила')
        #pygame.display.set_icon(pygame.image.load('data/mar_icon.png'))
        screen.blit(load_image('sky.png'), (0, 0))
        text = ['Игрок движется слева направо по экрану в попытках',
                'добраться до флага, означающего переход на следующий',
                'уровень. Вокруг Марио разбросаны монеты, а специальные',
                'кирпичи с вопросительным знаком могут увеличить',
                'количество монет, если итальянец ударится о них. Другие',
                'секретные кирпичи могут содержать больше монет или',
                'интересные бонусы. Игра заканчивается, когда',
                'герой травмируется, падает в яму']
        tille = pygame.font.SysFont('arial', 40).render('Правила игры:', True, (255, 255, 255))
        textRect = tille.get_rect()
        textRect.center = (400, 50)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            screen.blit(load_image('sky.png'), (0, 0))
            screen.blit(tille, textRect)
            for i in range(len(text)):
                line = ARIAL_50.render(text[i], True, (255, 255, 255))
                lineRect = line.get_rect()
                lineRect.center = (400, 90 + 25 * i)
                screen.blit(line, lineRect)
            pygame.display.flip()

    def chose_hero(self):
        pygame.display.set_caption('Выбор героя')
        pygame.display.set_icon(load_image('mar_icon.png'))
        screen.blit(load_image('sky.png'), (0, 0))
        mario = MarioChose(heros_sprites)
        luidzi = LuidziChose(heros_sprites)
        heros_sprites.draw(screen)
        running = True
        line = pygame.font.SysFont('arial', 40).render('Выберите героя', True, (255, 255, 255))
        lineRect = line.get_rect()
        lineRect.center = (400, 40)
        screen.blit(line, lineRect)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mario.rect.collidepoint(event.pos):
                        mario.update(event)
                        running = False
                    elif luidzi.rect.collidepoint(event.pos):
                        luidzi.update(event)
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            screen.blit(load_image('sky.png'), (0, 0))
            screen.blit(line, lineRect)
            heros_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            running = True
            #screen.blit(load_image('sky.png'), (0, 0))
            menu = Menu()
            menu.append_option('Правила игры', lambda: self.rules())
            menu.append_option('Рекорд', lambda: print('Рекорд'))
            menu.append_option('Выбор героя', lambda: self.chose_hero())

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        if event.key == 119:
                            menu.switch(-1)
                            print('w')
                        if event.key == 115:
                            menu.switch(1)
                            print('s')
                        if event.key == 13:
                            menu.select()

                screen.blit(load_image('sky.png'), (0, 0))
                menu.draw(screen, 300, 100, 40)
                pygame.display.flip()
                clock.tick(FPS)
            start()



if __name__ == '__main__':
    print(1)
    start()
