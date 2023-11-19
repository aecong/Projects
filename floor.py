from pico2d import *

import game_framework
from popcorn import Popcorn

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Floor:
    def __init__(self):
        self.x = 0
        self.image = load_image('resource/floor.png')

    def draw(self):
        self.image.draw(self.x, 250, 1600, 640)
        self.image.draw(self.x+1600, 250, 1600, 640)

    def update(self):
        if Popcorn.eat == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x <= -1600:
            self.x = 0
