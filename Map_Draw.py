from Heros_sprite import *


class Camera:
    def __init__(self, *sprites_need_start):
        from main import width
        self.dx = 0
        self.width = width
        self.x = 0
        self.sprites_need_start = sprites_need_start

    def update(self, obj, mario):
        if mario.rect.x > self.width // 2:
            self.dx = mario.rect.x - (self.width // 2)
            self.x += self.dx
            for el in obj:
                el.rect.x -= self.dx
        for el in self.sprites_need_start:
            if self.x == 0:
                start_sprite(el, self.width)
            else:
                start_sprite(el, mario.rect.x + self.width // 2)


class Map():
    def __init__(self, number):
        self.sp1 = [World_1, World_2]
        self.map = self.sp1[number - 1].map.copy()
        self.bonuss = self.sp1[number - 1].bonuses.copy()
        self.all_sprites = pygame.sprite.Group()
        self.first = pygame.sprite.Group()
        self.second = pygame.sprite.Group()
        self.notouch = pygame.sprite.Group()
        self.touch_but_nomove = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.play = pygame.sprite.Group()
        self.power = pygame.sprite.Group()
        self.ground = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.bonus = pygame.sprite.Group()
        self.brick = pygame.sprite.Group()
        self.ground_block = pygame.sprite.Group()
        self.tube = pygame.sprite.Group()
        self.zero = pygame.sprite.Group()
        self.pause = pygame.sprite.Group()
        self.win = pygame.sprite.Group()
        self.sp = [None, Cloud, Big_Cloud, Brick, Ground, Bush, Big_Bush, Hill, Big_Hill, Bonus, Tube_Small, Tube_Sr, Tube_Big,
            Block, Castle, None_tube, Turtle_Green, Mushrooms, Money, Mushroom_Power, Mario]

    def generate_level(self, hero):
        mario = None
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] in [1, 2, 5, 6, 7, 8]:
                    self.sp[self.map[y][x]](x, y, self.all_sprites, self.notouch, self.first)
                elif self.map[y][x] == 14:
                    self.sp[self.map[y][x]](x, y, self.all_sprites, self.notouch, self.first, self.win)
                elif self.map[y][x] in [10, 11, 12]:
                    self.sp[self.map[y][x]](x, y, self.all_sprites, self.ground_block, self.touch_but_nomove,
                                            self.first)
                    self.map = self.make_tube(self.map[y][x], x, y)
                elif self.map[y][x] == 9 and ((x != 0 and self.map[y][x - 1] == 0) or (x != len(self.map[y]) - 1 and self.map[y][x + 1] == 0)):
                    self.sp[self.map[y][x]](x, y, self.bonuss.pop(0), self.all_sprites, self.brick, self.bonus, self.ground,self.play, self.touch_but_nomove, self.first)
                elif self.map[y][x] == 9:
                    self.sp[self.map[y][x]](x, y, self.bonuss.pop(0), self.all_sprites, self.bonus, self.brick, self.ground, self.play, self.touch_but_nomove, self.first)
                elif self.map[y][x] in [3, 4]:
                    self.sp[self.map[y][x]](x, y, self.all_sprites, self.ground, self.brick, self.touch_but_nomove, self.first)
                elif self.map[y][x] == 13:
                    self.sp[self.map[y][x]](x, y, self.all_sprites, self.ground, self.brick, self.ground_block, self.touch_but_nomove, self.first)
                elif self.map[y][x] in [16, 17]:
                    self.sp[self.map[y][x]](x, y, [self.ground_block, self.ground, self.ground_block], self.enemy,  self.all_sprites, self.play, self.second)
                elif self.map[y][x] == 20:
                    mario = self.sp[self.map[y][x]](x, y, hero, [self.enemy, self.ground, self.brick, self.touch_but_nomove, self.ground_block, self.tube, self.win], self.all_sprites, self.player, self.second)
        return mario

    def make_tube(self, number,  x, y):
        for i in range(2):
            for j in range(number - 8):
                self.map[y - j][x + i] = 15
                self.sp[15](x + i, y - j, self.all_sprites, self.ground, self.brick, self.ground_block, self.touch_but_nomove, self.zero)
        self.map[y][x] = number
        return self.map


def start_game():
    from main import clock, FPS, Level, Hero
    maps = Map(Level + 1)
    mario = maps.generate_level(Hero)
    pausa = Pause(5, 10, maps.pause, maps.second)
    go_menu = In_Menu(5, 60, maps.pause, maps.second)
    camera = Camera(maps.enemy)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and pausa.rect.collidepoint(event.pos):
                t = pausa.clicked()
            elif event.type == pygame.MOUSEBUTTONDOWN and go_menu.rect.collidepoint(event.pos):
                running = False
                go_menu.clicked()
        pygame.display.flip()
        screen.fill((132, 132, 255))
        if mario.flag_die == 'kill':
            running = False
            game_over()
        else:
            points_and_coins(screen, mario.points, mario.coins)
            maps.bonus.draw(screen)
            maps.zero.draw(screen)
            maps.first.draw(screen)
            maps.second.draw(screen)
            if pausa.flag_not_paused:
                camera.update(maps.all_sprites, mario)
                key = pygame.key.get_pressed()
                mario.get_event(key, camera.x)
                if mario.update():
                    from main import EndGame
                    EndGame(mario.points, mario.coins)
                for el in maps.play:
                    el.play(camera.x)
            else: screen.blit(t, ((screen.get_width() - t.get_width()) // 2, (screen.get_height() - t.get_height()) // 2))
        clock.tick(FPS)


def game_over():
    screen.fill((0, 0, 0))
    t = text('game over', (255, 255, 255), 70)
    screen.blit(t, ((screen.get_width() - t.get_width()) // 2, (screen.get_height() - t.get_height()) // 2))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_game()
        pygame.display.flip()