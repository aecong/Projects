import math
import random

from pico2d import *

import game_framework
from cookie import Cookie


def time_out(e):
    return e[0] == 'TIME_OUT'
def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

POPCORN_SPEED_KMPH = 1.0
POPCORN_SPEED_MPM = POPCORN_SPEED_KMPH * 1000.0 / 60.0
POPCORN_SPEED_MPS = POPCORN_SPEED_MPM / 60.0
POPCORN_SPEED_PPS = POPCORN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class Popcorn:
    image = None
    popcorn_eat_sound = None
    eat = 0
    power = 1
    throwPower = 1
    def __init__(self):
        if Popcorn.image == None:
            self.image = load_image('resource/popcorn.png')
        self.x, self.y = random.randint(800, 1600), 200
        self.angle = 0
        self.font = load_font('resource/CookieRun Regular.TTF', 32)
        Popcorn.eat = 0
        self.updown = 0
        if not Popcorn.popcorn_eat_sound:
            Popcorn.popcorn_eat_sound = load_wav('resource/bgm_popcorn.wav')
            Popcorn.popcorn_eat_sound.set_volume(32)

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)

        if Popcorn.eat == 1:
            self.font.draw(self.x, self.y, f'{int(Popcorn.power):2d}', (255, 0, 255))
        elif Popcorn.eat == 2 or 3:
            self.font.draw(self.x, self.y, f'{int(Popcorn.throwPower):2d}', (255, 0, 255))


    def update(self):
        if Popcorn.eat == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time
        elif Popcorn.eat == 1:
            Popcorn.power += POPCORN_SPEED_PPS * game_framework.frame_time
            if Popcorn.power > 10:
                Popcorn.power = 1
        elif Popcorn.eat == 2:
            # global updown
            if self.updown == 0:
                self.y += RUN_SPEED_PPS * game_framework.frame_time
                if self.y > 400: self.updown = 1
            elif self.updown == 1:
                self.y -= RUN_SPEED_PPS * game_framework.frame_time
                if self.y < 200: self.updown = 0

        elif Popcorn.eat == 3:
            POWER_SPEED_KMPH = Popcorn.throwPower * 5
            POWER_SPEED_MPM = POWER_SPEED_KMPH * 1000.0 / 60.0
            POWER_SPEED_MPS = POWER_SPEED_MPM / 60.0
            POWER_SPEED_PPS = POWER_SPEED_MPS * PIXEL_PER_METER
            self.x += POWER_SPEED_PPS * game_framework.frame_time
            if self.x > 800:
                self.x, self.y = random.randint(800, 1600), 200
                Popcorn.eat = 0

        if self.x < -100:
            self.x, self.y = random.randint(800, 1600), 200
            Popcorn.eat = 0

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'cookie:popcorn':
            if Popcorn.eat == 0:
                Popcorn.popcorn_eat_sound.play()
                Popcorn.eat = 1
        elif group == 'popcorn:item':
                Cookie.itemCount += 1 * int(Popcorn.throwPower)
                return
