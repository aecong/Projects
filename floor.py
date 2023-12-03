from pico2d import *

import game_framework
from popcorn import Popcorn
from rod import Rod

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

ROD_SPEED_KMPH = 25.0
ROD_SPEED_MPM = ROD_SPEED_KMPH * 1000.0 / 60.0
ROD_SPEED_MPS = ROD_SPEED_MPM / 60.0
ROD_SPEED_PPS = ROD_SPEED_MPS * PIXEL_PER_METER

class Floor:
    image = None
    def __init__(self):
        self.x, self.y = -100, 250
        if Floor.image == None:
            self.image = load_image('resource/newfloor.png')
            self.obstacle = load_image('resource/obstacle_rod.png')
    def draw(self):
        self.image.draw(self.x, self.y, 800, 640)
        self.image.draw(self.x + 800, self.y, 800, 640)
        self.obstacle.draw(self.x + 75, self.y - 100, 100, 200)
        # draw_rectangle(*self.get_bb())

    def update(self):
        if Popcorn.eat == 0 or Rod.Mode == 0 or Rod.Mode == 2 or Rod.Mode == 3:
            if Rod.Mode == 2 or Rod.Mode == 3:
                self.x -= ROD_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.x <= -800:
            self.x = 0

    def get_bb(self):
        return self.x + 25, self.y - 200, self.x + 125, self.y - 50

    def handle_collision(self, group, other):
        if group == 'cookie:floor':
            pass
class Floorelseleft:
    def __init__(self):
        self.x, self.y = -100, 250

    def draw(self):
        # draw_rectangle(*self.get_bb())
        pass

    def update(self):
        if Popcorn.eat == 0 or Rod.Mode == 0 or Rod.Mode == 2 or Rod.Mode == 3:
            if Rod.Mode == 2 or Rod.Mode == 3:
                self.x -= ROD_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.x <= -800:
            self.x = 0

    def get_bb(self):
        return self.x + 125, self.y - 200, self.x + 825, self.y - 100
    def handle_collision(self, group, other):
        if group == 'cookie:nothole':
            pass
class nextFloor:
    image = None
    def __init__(self):
        self.x, self.y = 700, 250
        if nextFloor.image == None:
            self.image = load_image('resource/newfloor.png')
            self.obstacle = load_image('resource/obstacle_rod.png')

    def draw(self):
        self.image.draw(self.x, self.y, 800, 640)
        self.image.draw(self.x + 800, self.y, 800, 640)
        self.obstacle.draw(self.x + 75, self.y - 100, 100, 200)
        # draw_rectangle(*self.get_bb())

    def update(self):
        if Popcorn.eat == 0 or Rod.Mode == 0 or Rod.Mode == 2 or Rod.Mode == 3:
            if Rod.Mode == 2 or Rod.Mode == 3:
                self.x -= ROD_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.x <= 0:
            self.x = 800

    def get_bb(self):
        return self.x + 25, self.y - 200, self.x + 125, self.y - 50
    def handle_collision(self, group, other):
        if group == 'cookie:floor':
            pass
class nextFloorelse:
    def __init__(self):
        self.x, self.y = 700, 250

    def draw(self):
        # draw_rectangle(*self.get_bb())
        pass

    def update(self):
        if Popcorn.eat == 0 or Rod.Mode == 0 or Rod.Mode == 2 or Rod.Mode == 3:
            if Rod.Mode == 2 or Rod.Mode == 3:
                self.x -= ROD_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.x <= 0:
            self.x = 800

    def get_bb(self):
        return self.x + 125, self.y - 200, self.x + 675, self.y - 100
    def handle_collision(self, group, other):
        if group == 'cookie:nothole':
            pass
