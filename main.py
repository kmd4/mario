from Map_Draw import *
from Functions import *
import os.path

points = 0
size = width, height = 800, 482
heros_sprites = pygame.sprite.Group()
start_window_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
ARIAL_50 = pygame.font.SysFont('arial', 25)
clock = pygame.time.Clock()
FPS = 25
Hero = 'm'
Level = 0


def next_lev():
    global Level
    Level = (Level + 1) % 2


def data_result(points, coins):
    with open('data/result.txt', 'r', encoding='utf-8') as f1:
        result = f1.readline()
        points_f, coins_f = result.split()[0], result.split()[1]
        pointsmax = max(int(points_f), points)
        coins = int(coins_f) + coins
    with open('data/result.txt', 'w', encoding='utf-8') as f2:
        f2.write(f'{pointsmax} {coins}')
    return f'points: {points}  record: {pointsmax}'


def read_result():
    if os.path.exists('data/result.txt'):
        with open('data/result.txt', 'r', encoding='utf-8') as f1:
            result = f1.readline()
        with open('data/result.txt', 'w', encoding='utf-8') as f1:
            f1.write(result)
    else:
        with open('data/result.txt', 'w', encoding='utf-8') as f1:
            result = f"{0} {0}"
            f1.write(result)

    return f'points: {result.split()[0]} coins: {result.split()[1]}'


def start():
    global start_window_sprites
    start_window_sprites = pygame.sprite.Group()
    pygame.display.set_caption('Mario Bros')
    pygame.display.set_icon(load_image('mar_icon.png'))
    OpenMenu(start_window_sprites)
    StartGame(start_window_sprites)
    screen.blit(load_image('first_window.png', width=width, height=height), (0, 0))
    t = text(read_result(), (0, 130, 0), 30)
    screen.blit(t, (470, 20))
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
    terminate()


class EndGame:
    def __init__(self, p, c):
        Win_Game = pygame.sprite.Group()
        running = True
        ReGame(370, 300, Win_Game)
        StartGame1(430, 300, Win_Game)
        In_Menu(310, 300, Win_Game)
        self.sky_image = load_image('menu_image.png', width=width, height=height)
        screen.blit(self.sky_image, (0, 0))
        Win_Game.draw(screen)
        t = text('WIN', (0, 0, 0), 90)
        res = text(data_result(p, c), (0, 0, 0), 40)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Win_Game.update(event)

            screen.blit(self.sky_image, (0, 0))
            Win_Game.draw(screen)
            screen.blit(t, ((screen.get_width() - t.get_width()) // 2, 60))
            screen.blit(res, ((screen.get_width() - res.get_width()) // 2, 180))
            pygame.display.flip()
            clock.tick(FPS)
        terminate()


class StartGame(pygame.sprite.Sprite):
    image = load_image('start_game.png', color_key=-1, width=50, height=50)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = StartGame.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 375, 325

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            from Map_Draw import start_game
            start_game()


class MarioChose(pygame.sprite.Sprite):
    image = load_image('mmario.png')

    def __init__(self, x, y,  *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            global Hero
            Hero = 'm'


class LuidziChose(pygame.sprite.Sprite):
    image = load_image('lluidzi.png')

    def __init__(self, x, y,  *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

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
        self._option_surfaces.append(pygame.font.SysFont('arial', 40).render(option, True, (0, 0, 0)))
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
                pygame.draw.rect(surf, (250, 240, 230), option_rect)
            surf.blit(option, option_rect)


class OpenMenu(pygame.sprite.Sprite):
    image_menu = load_image('8.png', width=50, height=50)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = OpenMenu.image_menu
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 10, 10
        self.sky_image = load_image('menu_image.png', width=width, height=height)

    def rules(self):
        pygame.display.set_caption('Правила')
        screen.blit(self.sky_image, (0, 0))
        text = ['Игрок движется слева направо по экрану в попытках',
                'добраться до флага, означающего переход на следующий',
                'уровень. Вокруг Марио разбросаны монеты, а специальные',
                'кирпичи с вопросительным знаком могут увеличить',
                'количество монет, если итальянец ударится о них. Другие',
                'секретные кирпичи могут содержать больше монет или',
                'интересные бонусы. Игра заканчивается, когда',
                'герой травмируется, падает в яму']
        tille = pygame.font.SysFont('arial', 40).render('Правила игры:', True, (0, 0, 0))
        textRect = tille.get_rect()
        textRect.center = (400, 50)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            screen.blit(self.sky_image, (0, 0))
            screen.blit(tille, textRect)
            for i in range(len(text)):
                line = ARIAL_50.render(text[i], True, (0, 0, 0))
                lineRect = line.get_rect()
                lineRect.center = (400, 90 + 25 * i)
                screen.blit(line, lineRect)
            pygame.display.flip()

    def chose_hero(self):
        pygame.display.set_caption('Выбор героя')
        screen.blit(self.sky_image, (0, 0))
        mario = MarioChose(150, 50, heros_sprites)
        luidzi = LuidziChose(500, 50, heros_sprites)
        heros_sprites.draw(screen)
        running = True
        line = pygame.font.SysFont('arial', 40).render('Выберите героя', True, (0, 0, 0))
        lineRect = line.get_rect()
        lineRect.center = (400, 40)
        screen.blit(line, lineRect)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
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

            screen.blit(self.sky_image, (0, 0))
            screen.blit(line, lineRect)
            heros_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            running = True
            menu = Menu()
            menu.append_option('Правила игры', lambda: self.rules())
            menu.append_option(' Выбор героя ', lambda: self.chose_hero())

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        if event.key == 119:
                            menu.switch(-1)
                        if event.key == 115:
                            menu.switch(1)
                        if event.key == 13:
                            menu.select()

                screen.blit(self.sky_image, (0, 0))
                menu.draw(screen, 300, 150, 50)
                pygame.display.flip()
                clock.tick(FPS)
            start()

if __name__ == '__main__':
    start()
