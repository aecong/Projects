import math
import random

from pico2d import *

import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Popcorn:
    image = None
    popcorn_eat_sound = None
    eat = 0
    def __init__(self):
        if Popcorn.image == None:
            self.image = load_image('resource/popcorn.png')
        self.x, self.y = random.randint(800, 1600), 200
        self.power = 1
        Popcorn.eat = 0
        if not Popcorn.popcorn_eat_sound:
            Popcorn.popcorn_eat_sound = load_wav('resource/bgm_popcorn.wav')
            Popcorn.popcorn_eat_sound.set_volume(32)

    def draw(self):
        self.image.draw(self.x, 200, 100, 100)

        # draw_rectangle(*self.get_bb())

    def update(self):
        self.x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.x < -100:
            self.x = random.randint(800, 1600)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'cookie:popcorn':
            game_world.remove_object(self)
            Popcorn.popcorn_eat_sound.play()
            global popcorn
            popcorn = Popcorn()
            game_world.add_object(popcorn, 2)
            game_world.add_collision_pair('cookie:popcorn', None, popcorn)
            Popcorn.eat = 1
            pass