import math
import random

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
from cookie import Cookie
from popcorn import Popcorn

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Obstacle:
    image = None

    def __init__(self):
        if Obstacle.image == None:
            self.image = load_image('resource/obstacle.png')
        self.x, self.y = random.randint(400, 800), 200
        self.falldown = 0

    def draw(self):
        if self.falldown == 0:
            self.image.draw(self.x, 200, 150, 200)
        else:
            self.image.clip_composite_draw(0, 0, 150, 200, -math.pi / 2, '', self.x, 150, 150, 200)
        # draw_rectangle(*self.get_bb())

    def update(self):
        if Popcorn.eat == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.x < -150:
            self.x = random.randint(600, 1000)
            self.falldown = 0

    def get_bb(self):
        if self.falldown == 0:
            return self.x - 40, self.y - 100, self.x + 40, self.y + 10
        else:
            return self.x - 80, self.y - 100, self.x, self.y + 10


    def handle_collision(self, group, other):
        if group == 'cookie:obstacle':
            self.falldown = 1
            return