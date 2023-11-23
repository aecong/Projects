import math
import random

from pico2d import *

import game_framework
import game_world

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
    throwPower = None
    def __init__(self):
        if Popcorn.image == None:
            self.image = load_image('resource/popcorn.png')
        self.x, self.y = random.randint(800, 1600), 200
        self.power = 1
        self.font = load_font('resource/CookieRun Regular.TTF', 32)
        Popcorn.eat = 0
        if not Popcorn.popcorn_eat_sound:
            Popcorn.popcorn_eat_sound = load_wav('resource/bgm_popcorn.wav')
            Popcorn.popcorn_eat_sound.set_volume(32)

    def draw(self):
        self.image.draw(self.x, 200, 100, 100)
        # draw_rectangle(*self.get_bb())
        if Popcorn.eat == 1:
            self.font.draw(self.x, self.y + 60, f'{int(self.power):2d}', (255, 0, 255))

    def update(self):
        if Popcorn.eat == 1:
            self.power += POPCORN_SPEED_PPS * game_framework.frame_time
            if self.power > 10:
                self.power = 1

        elif Popcorn.eat == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x < -100:
            game_world.remove_object(self)
    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'cookie:popcorn':
            if Popcorn.eat == 0:
            # game_world.remove_object(self)
                Popcorn.popcorn_eat_sound.play()
            # global popcorn
            # popcorn = Popcorn()
            # game_world.add_object(popcorn, 2)
            # game_world.add_collision_pair('cookie:popcorn', None, popcorn)
            Popcorn.eat = 1
            pass