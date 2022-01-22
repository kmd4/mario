from Background_sprites import *


class Moving(pygame.sprite.Sprite):
    timer_kill = 0
    sheet = load_image('coin1.png')
    size = width, height = 32, 32
    columns, rows, a1, a2, b1, b2 = 0, 0, 0, 0, 0, 0 #for life
    columnsk, rowsk, a1k, a2k, b1k, b2k = 0, 0, 0, 0, 0, 0 #for kill
    offset_x, offset_y = 0, 34 #отступы
    speed_x, speed_y = 0, 0 #число кратно 32
    speed_start_game = 4
    g = 2

    def __init__(self, x, y, arg, *group):
        super().__init__(*group)
        self.arg = arg
        if self.columns != 0:
            self.frames = cut_sheet(self, self.sheet, self.columns, self.rows, self.a1, self.a2, self.b1, self.b2)
        if self.columnsk != 0:
            self.frames_die = cut_sheet(self, self.sheet, self.columnsk, self.rowsk, self.a1k, self.a2k, self.b1k, self.b2k)
        self.cur_frame, self.cur_kill_frame = 0, 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.offset = get_offset(self.image)
        self.offset_yy = min(map(lambda x: get_offset(x)[1], self.frames))
        self.offset_y += self.offset_yy
        self.rect.bottomleft = (self.width * x + self.offset_x, self.height * (y + 1) + self.offset_y)
        self.flag_fall = 0
        self.flag_kill = 0

    def kill_sprite(self):
        pass

    def play(self, offset):
        if self.flag_kill == 1:
            self.kill_sprite()
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            if collidepoint_by_mask(self, self.arg[2]) != []:
                self.speed_x = -self.speed_x
                self.frames = flip(self.frames)
                off = get_offset(self.image)
                self.first_step = off[3] - off[2]
                self.rect.x -= self.first_step
            h = get_nearest_block(self, self.height, offset)[0]
            if h == 'kill' or self.rect.x + self.width < 0:
                self.kill()
            else:
                if h[0] != None and h[0] > 0 and h[0] > self.offset_yy:
                    if self.speed_y + self.g < h[0]:
                        self.speed_y = self.speed_y + self.g
                    else:
                        self.speed_y = h[0]
                        self.flag_fall = 1
                elif self.flag_fall == 1:
                    self.flag_fall = 0
                    self.speed_y = 0
                elif h[0] == None:
                    self.speed_y += self.g
                if self.flag_kill == 1:
                    self.kill_sprite()
                    if self.timer_kill == 0:
                        self.speed_x, self.speed_y = 0, 0
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


class Mushrooms(Moving):
    time_for_kill = 50
    sheet = load_image('mush.png')
    columns, rows, a1, a2, b1, b2 = 9, 1, 0, 2, 0, 1
    columnsk, rowsk, a1k, a2k, b1k, b2k = 9, 1, 2, 3, 0, 1
    timer_kill = 10

    def kill_sprite(self):
        if self.timer_kill == 10:
            self.cur_kill_frame = (self.cur_kill_frame + 1) % len(self.frames_die)
            self.image = self.frames_die[self.cur_kill_frame]
            self.speed_x = 0
        elif self.timer_kill == 0:
            self.kill()
        self.timer_kill -= 1


class Mario(pygame.sprite.Sprite):
    sheet_m = load_image('mario_L.png')
    sheet_l = load_image('luigi_L.png')
    size = width, height = 32, 32
    offset_x, offset_y = 0, 34  # отступы
    speed_x, speed_y = 0, 0  # число кратно 32
    g = 2
    direct = 1

    def __init__(self, x, y, flag, arg, *group): #flag 'm' - mario, 'l' - luigi
        super().__init__(*group)
        self.arg = arg
        self.framesm = cut_sheet(self, self.sheet_m, 7, 1, 0, 7, 0, 1)
        self.framesl = cut_sheet(self, self.sheet_l, 7, 1, 0, 7, 0, 1)
        self.distin = {'m': self.framesm, 'l': self.framesl}
        self.cur_frames = self.distin.get(flag)
        self.cur_frame = 0
        self.image = self.cur_frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.width * x + self.offset_x, self.height * (y + 1) + self.offset_y)
        self.speed_jump = 16
        self.speed_die = -16
        self.max_jump_height = 2.5 * self.width // self.speed_jump
        self.flag_jump = 0
        self.flag_stay = False
        self.flag_die = False
        self.points, self.coins = 0, 0

    def get_event(self, key, off):
        if not self.flag_die:
            h = get_nearest_block(self, self.width, off, param=True)
            if len(h) == 1:
                self.flag_die = 1
            else:
                self.h, self.h1, self.h2, self.h3 = h
            if key == 'KEYUP' and self.flag_jump == 1:
                self.flag_jump = key
            elif key != 'KEYUP':
                if not (key[pygame.K_RIGHT] or key[pygame.K_d] or key[pygame.K_LEFT] or key[pygame.K_a]):
                    self.speed_x = 0
                if (key[pygame.K_UP] or key[pygame.K_w]) and self.flag_jump == 0:
                    self.flag_jump = 1
                if not (key[pygame.K_UP] or key[pygame.K_w]) and self.flag_jump == 1:
                    self.flag_jump = 2
                if (key[pygame.K_RIGHT] or key[pygame.K_d]) and (self.flag_stay == 0 or self.rect.x == 0):
                    be, self.direct = self.direct, 1
                    self.run(be)
                elif self.rect.x == 0:
                    self.stand()
                elif key[pygame.K_LEFT] or key[pygame.K_a]:
                    be, self.direct = self.direct, -1
                    self.run(be)

    def update(self):
        if collidepoint_by_mask(self, self.arg[6]):
            return True
        k = collidepoint_by_mask(self, self.arg[0])
        if k and self.flag_jump in [2, 3] and up_mask(self, k[0]):
            k[0].flag_kill = 1
            self.points += 100
            self.flag_jump = 1
            self.max_jump_height = 1 * self.width // self.speed_jump
        elif k and k[0].flag_kill == 0:
            self.flag_die = 1
            self.speed_x = 0
        if self.flag_die == 1:
            self.die()
        else:
            if self.flag_jump in [1, 2, 3]:
                self.jump()
            elif self.speed_y == 0 and self.speed_x == 0 and self.flag_jump == 0 and self.flag_die == 0:
                self.stand()
            if self.flag_jump == 0:
                if self.h[0] != 0:
                    self.flag_jump = 2
                    self.jump()
            self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def die(self):
        self.image = self.cur_frames[1]
        if self.rect.y <= self.offset_y + 14 * self.height:
            self.speed_die += self.g
            self.speed_y = self.speed_die
        else:
            self.flag_die = 'kill'
            self.kill()

    def jump(self):
        self.image = self.cur_frames[-1]
        s = [self.speed_jump, self.h1[0]]
        while None in s:
            s.pop(s.index(None))
        if self.h[0] == 0 and self.flag_jump != 1:
            self.speed_y = 0
            self.flag_jump = 0
            self.max_jump_height = 2.5 * self.width // self.speed_jump
        elif self.h1[0] == 0:
            self.speed_y = 0
            self.flag_jump = 2
            if self.h1[1] == 9:
                self.rect.y -= 1
                self.points += 130
                self.coins += 1
        elif self.max_jump_height == 0:
            self.flag_jump = 2
        elif (self.speed_y == self.speed_jump or self.rect.x <= 0) and self.flag_jump == 2:
            self.flag_jump = 3
        if self.flag_jump == 1 and self.max_jump_height != 0:
            self.speed_y = -min(s)
            self.max_jump_height -= 1
        elif self.flag_jump == 2 and self.speed_y != self.speed_jump:
            if self.speed_y <= -self.g and self.h1[0] != None and self.h1[0] > 0:
                self.speed_y = max(self.speed_y + self.g, -self.h1[0])
            elif self.h[0] == None:
                self.speed_y += self.g
            else:
                self.speed_y = min(self.speed_y + self.g, self.h[0])
        elif self.flag_jump == 3:
            if self.h[0] != None: self.speed_y = min(self.speed_jump, self.h[0])
            else: self.speed_y = self.speed_jump

    def run(self, be):
        if self.direct == 1:
            if self.h3[0] != None: self.speed_x = min(8, self.h3[0])
            else: self.speed_x = 8
        else:
            if self.h2[0] != None: self.speed_x = min(8, self.h2[0]) * self.direct
            else: self.speed_x = -8
        if be != self.direct:
            self.cur_frames = flip(self.cur_frames)
        run_frames = self.cur_frames[3:6]
        self.cur_frame = (self.cur_frame + 1) % len(run_frames)
        self.image = run_frames[self.cur_frame]

    def stand(self):
        self.image = self.cur_frames[0]
        self.speed_x = 0
        self.speed_y = 0
        self.cur_frame = 0


class Mushroom_Power(Moving):
    sheet = load_image('mush_power.png')
    columns, rows, a1, a2, b1, b2 = 0, 0, 0, 0, 0, 0


class Money(Moving):
    pass