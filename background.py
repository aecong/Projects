from pico2d import *

import game_framework
from cookie import Cookie

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 40.0 + Cookie.speed
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Background:
    def __init__(self):
        self.x = 0
        self.image = load_image('resource/back1.png')

    def draw(self):
        self.image.draw(self.x, 300, 2834, 638)
        self.image.draw(self.x+2834, 300, 2834, 638)

    def update(self):
        self.x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.x <= -2834:
            self.x = 0
