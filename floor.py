from pico2d import *

import game_framework
from popcorn import Popcorn

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Floor:
    def __init__(self):
        self.x, self.y = 0, 250
        self.image = load_image('resource/newfloor.png')

    def draw(self):
        self.image.draw(self.x, self.y, 800, 640)
        draw_rectangle(*self.get_bb())

    def update(self):
        if Popcorn.eat == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x <= -800:
            self.x = 0

    def get_bb(self):
        return self.x + 25, self.y - 200, self.x + 125, self.y - 100

    def handle_collision(self, group, other):
        if group == 'cookie:floor':
            print('충돌')

class nextFloor:
    image = None
    def __init__(self):
        self.x, self.y = 800, 250
        if nextFloor.image == None:
            self.image = load_image('resource/newfloor.png')

    def draw(self):
        self.image.draw(self.x, self.y, 800, 640)
        draw_rectangle(*self.get_bb())

    def update(self):
        if Popcorn.eat == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x <= 0:
            self.x = 800

    def get_bb(self):
        return self.x + 25, self.y - 200, self.x + 125, self.y - 100

    def handle_collision(self, group, other):
        if group == 'cookie:floor':
            print('충돌')

class thirdFloor:
    image = None
    def __init__(self):
        self.x, self.y = 1600, 250
        if nextFloor.image == None:
            self.image = load_image('resource/newfloor.png')

    def draw(self):
        self.image.draw(self.x, self.y, 800, 640)
        draw_rectangle(*self.get_bb())

    def update(self):
        if Popcorn.eat == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x <= 800:
            self.x = 1600

    def get_bb(self):
        return self.x + 25, self.y - 200, self.x + 125, self.y - 100

    def handle_collision(self, group, other):
        if group == 'cookie:floor':
            print('충돌')