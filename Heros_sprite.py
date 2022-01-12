from Functions import *
import pygame



class Moving(pygame.sprite.Sprite):
    timer_kill = 0
    sheet = load_image('coin1.png')
    size = width, height = 32, 32
    columns, rows, a1, a2, b1, b2 = 0, 0, 0, 0, 0, 0 #for life
    columnsk, rowsk, a1k, a2k, b1k, b2k = 0, 0, 0, 0, 0, 0 #for kill
    offset_x, offset_y = 0, 34 #отступы
    speed_x, speed_y = 4, 0 #число кратно 32
    g = 2

    def __init__(self, x, y, arg, *group):
        super().__init__(*group)
        self.arg = arg
        self.frames = cut_sheet(self, self.sheet, self.columns, self.rows, self.a1, self.a2, self.b1, self.b2)
        self.frames_die = cut_sheet(self, self.sheet, self.columnsk, self.rowsk, self.a1k, self.a2k, self.b1k, self.b2k)
        self.cur_frame, self.cur_kill_frame = 0, 0
        self.image = self.frames[self.cur_frame]
        self.image_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image_mask.get_rect()
        self.offset = get_offset(self.image)
        self.offset_yy = min(map(lambda x: get_offset(x)[1], self.frames))
        self.offset_y += self.offset_yy
        self.rect.bottomleft = (self.width * x + self.offset_x, self.height * (y + 1) + self.offset_y)
        self.flag_fall = 0
        self.flag_kill = 0

    def kill_sprite(self):
        pass


    def play(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if collidepoint_by_mask(self, self.arg[0]) != []:
            self.speed_x = -self.speed_x
            self.frames = flip(self.frames)
            off = get_offset(self.image)
            self.first_step = off[3] - off[2]
            self.rect.x -= self.first_step
        h = get_nearest_block(self, self.speed_x, 32)
        if h != None and h > 0 and h > self.offset_yy:
            if self.speed_y + self.g < h:
                self.speed_y = self.speed_y + self.g
            else:
                self.speed_y = h
                self.flag_fall = 1
        elif self.flag_fall == 1:
            self.flag_fall = 0
            self.speed_y = 0
        elif h == None:
            self.speed_y += self.g
        if self.flag_kill == 1:
            self.kill_sprite()
            if self.timer_kill == 0:
                self.kill()
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y



class Turtle_Green(Moving):
    sheet = load_image('turtle.png')
    columns, rows, a1, a2, b1, b2 = 6, 3, 2, 4, 0, 1
    columnsk, rowsk, a1k, a2k, b1k, b2k = 6, 3, 4, 6, 0, 1
    timer_kill = 5

    def kill_sprite(self):
        self.image = self.frames_die[0]
        self.speed_x = 0
        if self.timer_kill > 1:
            self.timer_kill -= 1
        elif self.timer_kill == 1:
            self.frames = [self.frames_die[1]]
            self.cur_frame = 0
            self.speed_x = -32
            self.flag_kill = 0
        print(self.timer_kill)





class Mushrooms(Moving):
    time_for_kill = 50
    sheet = load_image('mush.png')
    columns, rows, a1, a2, b1, b2 = 9, 1, 0, 2, 0, 1
    columnsk, rowsk, a1k, a2k, b1k, b2k = 9, 1, 2, 3, 0, 1
    timer_kill = 10

    def kill_sprite(self):
        self.cur_kill_frame = (self.cur_kill_frame + 1) % len(self.frames_die)
        self.timer_kill -= 1
        self.image = self.frames_die[self.cur_kill_frame]
        self.speed_x = 0


class Flag(Moving):
    sheet = load_image('flag_end.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = self.sheet
        self.rect = self.rect.move(x, y)

    def play(self):
        self.rect.y += 10


class Mario(pygame.sprite.Sprite):
    sheet_L = load_image('mario_L.png')
    sheet_B = load_image('mario_B.png')
    sheet_P = load_image('mario_p.png')
    columnsL, rowsL, a1L, a2L, b1L, b2L = 0, 0, 0, 0, 0, 0  # for little
    columnsB, rowsB, a1B, a2B, b1B, b2B = 0, 0, 0, 0, 0, 0  # for big
    columnsP, rowsP, a1P, a2P, b1P, b2P = 0, 0, 0, 0, 0, 0  # for big and perfect
    flag_mario_size = 'L'
    size = width, height = 32, 32
    offset_x, offset_y = 0, 34  # отступы
    speed_x, speed_y = 4, 4  # число кратно 32
    g = 2

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.framesL = cut_sheet(self, self.sheet_L, 7, 1, 0, 7, 0, 1)
        self.framesB = cut_sheet(self, self.sheet_B, 7, 1, 0, 7, 0, 1)
        self.framesP = cut_sheet(self, self.sheet_P, 7, 1, 0, 7, 0, 1)
        self.cur_frame = 0
        self.image = self.framesL[self.cur_frame]
        self.image_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image_mask.get_rect()
        self.rect.bottomleft = (self.width * x + self.offset_x, self.height * (y + 1) + self.offset_y)

    def get_event(self, key):  # Обработка событий
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.jump()
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            self.fall()
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.run(1)
        elif key[pygame.K_LEFT] or key[pygame.K_a]:
            self.run(-1)

    def jump(self):
        self.rect.y -= self.speed_y
        print('j')


    def fall(self):
        self.rect.y += self.speed_y
        print('f')

    def run(self, s):
        self.rect.x += self.speed_x * s


class Luigi(Mario):
    sheet = load_image('luigi.png')