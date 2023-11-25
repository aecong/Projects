import math
import random

from pico2d import *

import game_framework
from cookie import Cookie
from popcorn import Popcorn

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
FRAMES_PER_ACTION = 4

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class Rod:
    image = None
    def __init__(self):
        if Rod.image == None:
            self.image = load_image('resource/rod.png')
        self.x, self.y = 290, 200
        self.frame = 0

    def draw(self):
        if Popcorn.eat == 1:
            self.image.clip_draw(int(self.frame) * 851, 0, 851, 101, self.x, self.y, 340, 40)


    def update(self):
        self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4

